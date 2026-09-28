from __future__ import annotations

from collections import defaultdict

from rdkit import Chem

from ..basic import Molecule
from ..configs.reaction_center_extraction_configs import ExtractionConfig
from ..rules.expandable_functional_groups import (
    EXPANDABLE_FUNCTIONAL_GROUPS_COLLECTION,
)
from .errors.extraction_errors import ExtractionError
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
        self.include_stereo_tags = config.include_stereo_tags

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
                (idx in self._core_indices or atom.GetAtomMapNum() == 0)
                and atom.GetFormalCharge() == 0
            ) or atom.GetSymbol() == "H":
                smarts: str = atom.GetSmarts()
            else:
                smarts = clean_hydrogens_from_smarts(
                    atom.GetSmarts(), keep_stars=self.include_stereo_tags
                )
            # cover case when atom is valid as smiles but not as smarts
            # for example, in reagent CCC[CH2][Sn]([CH2]CCC)([CH2]CCC)[O][Ts]
            try:
                new_idx: int = fragment.AddAtom(Chem.AtomFromSmarts(smarts))
            except RuntimeError:
                raise ExtractionError(f"Failed to add atom {smarts} to fragment")
            atom_mapping[idx] = new_idx

            new_atom = fragment.GetAtomWithIdx(new_idx)
            new_atom.SetIsAromatic(atom.GetIsAromatic())
            new_atom.SetFormalCharge(atom.GetFormalCharge())
            new_atom.SetAtomMapNum(atom.GetAtomMapNum())
            new_atom.SetChiralTag(
                atom.GetChiralTag()
                if self.include_stereo_tags
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

        if self.include_stereo_tags:
            self._drop_truncated_stereo_tags(fragment, atom_mapping)
            self._drop_unperceived_context_stereo_tags(fragment, atom_mapping)

        return fragment.GetMol(), expanded_indices

    def _drop_unperceived_context_stereo_tags(
        self,
        fragment: Chem.RWMol,
        atom_mapping: dict[int, int],
    ) -> None:
        """Apply RDKit's stereo perception to context atoms, but not to core ones.

        Core atoms bypass stereo perception: telling retention from inversion is
        the whole point of recording stereochemistry on a reaction center, and at
        RC1 their substituents are truncated so heavily that RDKit no longer
        perceives them as stereocentres at all. Truncation can still clear a core
        tag when the atom's degree drops (see ``_drop_truncated_stereo_tags``).

        For the surrounding atoms that perception is the desired behaviour — a tag
        that survives it describes the fragment, one that does not is noise which
        would split otherwise identical centers.

        :param fragment: Fragment under construction, modified in place.
        :type fragment: Chem.RWMol
        :param atom_mapping: Parent atom index → fragment atom index.
        :type atom_mapping: dict[int, int]
        """
        tagged_context = [
            fragment_idx
            for parent_idx, fragment_idx in atom_mapping.items()
            if parent_idx not in self._core_indices
            and fragment.GetAtomWithIdx(fragment_idx).GetChiralTag()
            != Chem.ChiralType.CHI_UNSPECIFIED
        ]
        if not tagged_context:
            return

        # No perception verdict means no grounds to drop anything, so the tags
        # stay: an unreadable fragment must not silently lose stereochemistry.
        perceived = self._perceived_stereo_atoms(fragment)
        if perceived is None:
            return

        for fragment_idx in tagged_context:
            if fragment_idx not in perceived:
                fragment.GetAtomWithIdx(fragment_idx).SetChiralTag(
                    Chem.ChiralType.CHI_UNSPECIFIED
                )

    @staticmethod
    def _perceived_stereo_atoms(fragment: Chem.RWMol) -> set[int] | None:
        """Return indices RDKit perceives as stereocentres in *fragment*.

        Fragments are query molecules assembled atom by atom, so they carry
        neither an implicit-valence cache nor ring information, both of which
        perception needs.

        :param fragment: Fragment to inspect; not modified.
        :type fragment: Chem.RWMol
        :return: Perceived stereocentre indices, or *None* if RDKit cannot
            perceive stereochemistry for this fragment at all.
        :rtype: set[int] | None
        """
        probe = Chem.RWMol(fragment)
        try:
            probe.UpdatePropertyCache(strict=False)
            Chem.FastFindRings(probe)
            return {
                element.centeredOn
                for element in Chem.FindPotentialStereo(probe)
                if element.type == Chem.StereoType.Atom_Tetrahedral
            }
        except (RuntimeError, ValueError):
            return None

    def _drop_truncated_stereo_tags(
        self,
        fragment: Chem.RWMol,
        atom_mapping: dict[int, int],
    ) -> None:
        """Clear stereo tags from atoms that lost a substituent during extraction.

        A tetrahedral tag describes an arrangement of four substituents, so it
        only carries meaning while all of them are still attached. Extraction can
        drop one (a neighbour left outside the fragment, or a bond removed by
        :meth:`_should_skip_bond`), which would leave behind a tag that denotes
        nothing and can even be written out as an impossible atom such as
        ``[C@H3]``.

        Substituents that are merely *truncated* — a phenyl shortened to a single
        aromatic atom, say — do not count as lost: the atom keeps its degree and
        the tag still describes the original arrangement.

        :param fragment: Fragment under construction, modified in place.
        :type fragment: Chem.RWMol
        :param atom_mapping: Parent atom index → fragment atom index.
        :type atom_mapping: dict[int, int]
        """
        mol = self._safe_rdmol

        for parent_idx, fragment_idx in atom_mapping.items():
            fragment_atom = fragment.GetAtomWithIdx(fragment_idx)
            if fragment_atom.GetChiralTag() == Chem.ChiralType.CHI_UNSPECIFIED:
                continue

            if fragment_atom.GetDegree() < mol.GetAtomWithIdx(parent_idx).GetDegree():
                fragment_atom.SetChiralTag(Chem.ChiralType.CHI_UNSPECIFIED)
