from __future__ import annotations

from collections import defaultdict

from rdkit import Chem

from ..basic import Molecule
from ..configs.reaction_center_extraction_configs import ExtractionConfig
from ..rules.expandable_functional_groups import (
    EXPANDABLE_FUNCTIONAL_GROUPS_COLLECTION,
)
from .errors.fragment_extractor_errors import MoleculeNotSetError
from .utils import clean_hydrogens_from_smarts


class MolecularFragmentExtractor:
    """Extracts molecular fragments based on atom indices with configurable expansion.

    The extractor starts from a set of core atom indices and progressively
    expands the fragment by adding neighbours, ring atoms, fused systems,
    substituents, chiral centres and functional-group atoms according to
    the configuration supplied at construction time.
    """

    def __init__(self, config: ExtractionConfig) -> None:
        """
        Initialize the extractor from an extraction configuration.

        :param config: Extraction configuration.
        :type config: ExtractionConfig
        """
        self.neighbor_depth = config.neighbor_depth
        self.include_rings = config.include_rings
        self.include_fused = config.include_fused
        self.include_substituents = config.include_substituents
        self.include_chiral = config.include_chiral

        # Mutable state — reset before each extraction
        self._mol: Molecule | None = None
        self._core_indices: set[int] = set()
        self._all_indices: set[int] = set()
        self._ring_sets: list[set[int]] = []
        self._atom_to_rings: defaultdict[int, set[int]] = defaultdict(set)

    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------

    def _reset_state(self) -> None:
        """Reset internal state for a new extraction."""
        self._mol = None
        self._core_indices = set()
        self._all_indices = set()
        self._ring_sets = []
        self._atom_to_rings = defaultdict(set)

    @property
    def _safe_mol(self) -> Molecule:
        """Return the Molecule, raising if not set.

        :raises MoleculeNotSetError: If called before :meth:`extract_fragment`.
        :rtype: Molecule
        """
        if self._mol is None:
            raise MoleculeNotSetError()
        return self._mol

    @property
    def _safe_rdmol(self) -> Chem.Mol:
        """Return the atom-mapped canonical RDKit Mol via the stored Molecule.

        :raises MoleculeNotSetError: If called before :meth:`extract_fragment`.
        :rtype: Chem.Mol
        """
        return self._safe_mol.atom_mapped_canonical_rdmol

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract_fragment(
        self,
        mol: Molecule,
        atom_indices: list[int],
    ) -> tuple[Chem.Mol, list[int]]:
        """Extract a molecular fragment based on specified atom indices.

        :param mol: Molecule to extract the fragment from.
        :type mol: Molecule
        :param atom_indices: Atom indices that form the fragment core.
        :type atom_indices: list[int]
        :return: ``(fragment_mol, expanded_indices)`` — the fragment (atom maps
            copied from ``mol.atom_mapped_canonical_rdmol``) and the sorted list
            of all atom indices included in it (indices refer to that mol).
        :rtype: tuple[Chem.Mol, list[int]]
        """
        self._reset_state()

        if mol is None:
            raise MoleculeNotSetError()

        self._mol = mol
        self._core_indices = set(atom_indices)
        self._all_indices = set(atom_indices)

        self._find_rings()
        self._add_neighbors()
        self._add_unmapped_atoms()

        if self.include_rings:
            self._add_ring_atoms()

        if self.include_chiral:
            self._add_chiral_atoms()

        self._add_functional_group_atoms()

        return self._create_fragment_molecule()

    # ------------------------------------------------------------------
    # Ring detection
    # ------------------------------------------------------------------

    def _find_rings(self) -> None:
        """Identify all rings and build atom → ring-index mapping."""
        mol = self._safe_rdmol
        for ring in mol.GetRingInfo().AtomRings():
            ring_atoms: set[int] = set(ring)
            ring_idx = len(self._ring_sets)
            self._ring_sets.append(ring_atoms)
            for atom_idx in ring_atoms:
                self._atom_to_rings[atom_idx].add(ring_idx)

    # ------------------------------------------------------------------
    # Neighbour expansion
    # ------------------------------------------------------------------

    def _add_neighbors(self) -> None:
        """Expand the fragment by adding neighbouring atoms up to
        ``neighbor_depth``."""
        mol = self._safe_rdmol
        current_shell: set[int] = self._core_indices.copy()

        for _ in range(self.neighbor_depth):
            if not current_shell:
                break

            next_shell: set[int] = set()
            for idx in current_shell:
                for neighbor in mol.GetAtomWithIdx(idx).GetNeighbors():
                    nei_idx: int = neighbor.GetIdx()
                    if nei_idx not in self._all_indices:
                        self._all_indices.add(nei_idx)
                        next_shell.add(nei_idx)

            current_shell = next_shell

    def _add_unmapped_atoms(self) -> None:
        """Recursively add all unmapped neighbouring atoms."""
        mol = self._safe_rdmol
        found_new = True

        while found_new:
            found_new = False
            for idx in list(self._all_indices):
                for neighbor in mol.GetAtomWithIdx(idx).GetNeighbors():
                    nei_idx: int = neighbor.GetIdx()
                    if (
                        nei_idx not in self._all_indices
                        and neighbor.GetAtomMapNum() == 0
                    ):
                        self._all_indices.add(nei_idx)
                        found_new = True

    # ------------------------------------------------------------------
    # Ring expansion
    # ------------------------------------------------------------------

    def _add_ring_atoms(self) -> None:
        """Add ring, fused-system and substituent atoms to the fragment."""
        ring_atoms = self._collect_ring_atoms()

        if self.include_fused and ring_atoms:
            ring_atoms |= self._collect_fused_atoms(ring_atoms)

        if self.include_substituents:
            ring_atoms |= self._collect_ring_substituents(ring_atoms)

        self._all_indices |= ring_atoms

    def _collect_ring_atoms(self) -> set[int]:
        """Collect atoms from rings that overlap the current fragment.

        Non-aromatic, non-core, non-chiral atoms are skipped to avoid
        pulling in irrelevant saturated rings.

        :return: Set of atom indices belonging to relevant rings.
        :rtype: set[int]
        """
        mol = self._safe_rdmol
        result: set[int] = set()

        for atom_idx in self._all_indices:
            atom = mol.GetAtomWithIdx(atom_idx)
            if (
                not atom.GetIsAromatic()
                and atom_idx not in self._core_indices
                and atom.GetChiralTag() == Chem.ChiralType.CHI_UNSPECIFIED
            ):
                continue

            for ring_idx in self._atom_to_rings[atom_idx]:
                result |= self._ring_sets[ring_idx]

        return result

    def _collect_fused_atoms(self, ring_atoms: set[int]) -> set[int]:
        """Collect atoms from rings fused to *ring_atoms*.

        :param ring_atoms: Set of atom indices already identified as ring atoms.
        :type ring_atoms: set[int]
        :return: Additional atom indices from fused ring systems.
        :rtype: set[int]
        """
        result: set[int] = set()
        for atom_idx in ring_atoms:
            for ring_idx in self._atom_to_rings[atom_idx]:
                for ring_atom_idx in self._ring_sets[ring_idx]:
                    if ring_atom_idx not in self._all_indices:
                        result.add(ring_atom_idx)
        return result

    def _collect_ring_substituents(self, ring_atoms: set[int]) -> set[int]:
        """Collect non-ring neighbours of aromatic ring atoms.

        :param ring_atoms: Set of atom indices belonging to rings.
        :type ring_atoms: set[int]
        :return: Atom indices for substituents attached to aromatic ring atoms.
        :rtype: set[int]
        """
        mol = self._safe_rdmol
        substituents: set[int] = set()

        for atom_idx in ring_atoms:
            atom = mol.GetAtomWithIdx(atom_idx)
            if not atom.GetIsAromatic():
                continue
            for neighbor in atom.GetNeighbors():
                nei_idx: int = neighbor.GetIdx()
                bond = mol.GetBondBetweenAtoms(atom_idx, nei_idx)
                if bond is None:
                    continue
                if (
                    nei_idx not in self._all_indices
                    and nei_idx not in ring_atoms
                    and bond.GetBondType() != Chem.BondType.AROMATIC
                ):
                    substituents.add(nei_idx)

        return substituents

    # ------------------------------------------------------------------
    # Chiral-centre expansion
    # ------------------------------------------------------------------

    def _add_chiral_atoms(self) -> None:
        """Include rings and neighbours of chiral centres in the fragment."""
        mol = self._safe_rdmol
        atoms_to_add: set[int] = set()

        for atom_idx in list(self._all_indices):
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetChiralTag() == Chem.ChiralType.CHI_UNSPECIFIED:
                continue

            for ring_idx in self._atom_to_rings[atom_idx]:
                atoms_to_add |= self._ring_sets[ring_idx]

            for neighbor in atom.GetNeighbors():
                nei_idx: int = neighbor.GetIdx()
                if nei_idx not in self._all_indices:
                    atoms_to_add.add(nei_idx)

        self._all_indices |= atoms_to_add

    # ------------------------------------------------------------------
    # Functional-group expansion
    # ------------------------------------------------------------------

    def _add_functional_group_atoms(self) -> None:
        """Expand the fragment to include complete functional groups.

        If any atom of a matched functional-group pattern is already
        in the fragment, all atoms of that group are added.
        """
        mol = self._safe_mol

        matched_groups = (
            EXPANDABLE_FUNCTIONAL_GROUPS_COLLECTION.identify_functional_groups(mol)
        )
        for matched_group in matched_groups:
            for match_set in matched_group.matching_sets:
                if not self._all_indices.isdisjoint(match_set):
                    self._all_indices.update(match_set)

    # ------------------------------------------------------------------
    # Fragment construction
    # ------------------------------------------------------------------

    def _should_skip_bond(self, begin_idx: int, end_idx: int) -> bool:
        """Decide whether a bond should be omitted from the fragment.

        When ``include_rings`` is *False*, bonds between two mapped
        non-terminal atoms that are not in the core are skipped to
        disconnect mapped neighbours of reacting atoms.

        :param begin_idx: Index of the bond's begin atom.
        :type begin_idx: int
        :param end_idx: Index of the bond's end atom.
        :type end_idx: int
        :return: *True* if the bond should be skipped.
        :rtype: bool
        """
        if self.neighbor_depth != 1:
            return False

        if self.include_rings:
            return False

        if self._core_indices & {begin_idx, end_idx}:
            return False

        mol = self._safe_rdmol
        begin_atom = mol.GetAtomWithIdx(begin_idx)
        end_atom = mol.GetAtomWithIdx(end_idx)

        return (
            begin_atom.GetAtomMapNum() != 0
            and end_atom.GetAtomMapNum() != 0
            and begin_atom.GetDegree() != 1
            and end_atom.GetDegree() != 1
        )

    def _create_fragment_molecule(self) -> tuple[Chem.Mol, list[int]]:
        """Build an RDKit Mol from the accumulated atom indices.

        Atom map numbers are copied from the parent mol (``0`` if unmapped).

        :return: ``(fragment_mol, expanded_indices)``.
        :rtype: tuple[Chem.Mol, list[int]]
        """
        mol = self._safe_rdmol
        expanded_indices: list[int] = sorted(self._all_indices)

        fragment: Chem.RWMol = Chem.RWMol(Chem.Mol())
        atom_mapping: dict[int, int] = {}

        # --- Add atoms ---
        for idx in expanded_indices:
            atom = mol.GetAtomWithIdx(idx)

            if (
                idx in self._core_indices or atom.GetAtomMapNum() == 0
            ) and atom.GetFormalCharge() == 0:
                smarts: str = atom.GetSmarts()
            else:
                smarts = clean_hydrogens_from_smarts(
                    atom.GetSmarts(), keep_stars=self.include_chiral
                )

            new_idx: int = fragment.AddAtom(Chem.AtomFromSmarts(smarts))
            atom_mapping[idx] = new_idx

            new_atom = fragment.GetAtomWithIdx(new_idx)
            new_atom.SetIsAromatic(atom.GetIsAromatic())
            # Ignore formal charges
            new_atom.SetFormalCharge(0)
            new_atom.SetAtomMapNum(atom.GetAtomMapNum())
            new_atom.SetChiralTag(
                atom.GetChiralTag()
                if self.include_chiral
                else Chem.ChiralType.CHI_UNSPECIFIED
            )

        # --- Add bonds ---
        for bond in mol.GetBonds():
            begin_idx: int = bond.GetBeginAtomIdx()
            end_idx: int = bond.GetEndAtomIdx()

            if begin_idx not in atom_mapping or end_idx not in atom_mapping:
                continue

            if self._should_skip_bond(begin_idx, end_idx):
                continue

            fragment.AddBond(
                atom_mapping[begin_idx],
                atom_mapping[end_idx],
                bond.GetBondType(),
            )

        return fragment.GetMol(), expanded_indices
