from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from frozendict import frozendict
from rdkit import Chem
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers
from rdkit.Chem.EnumerateStereoisomers import StereoEnumerationOptions

from .errors.molecule_stereo_specification_errors import (
    MoleculeStereoSpecificationRuntimeError,
)


PSEUDO_CHIRAL_ATOMS_SMARTS_FILTERS = (
    Chem.MolFromSmarts("[#7,*$([*][Li,Na,K])]"),
    Chem.MolFromSmarts("[Ax3$([C,N]([CH2][CH2][C,N]1)([CH2][CH2]1))]"),
    Chem.MolFromSmarts("[Ax3$([C,N]([CH2][C,N]1)([CH2]1))]"),
    Chem.MolFromSmarts("[Ax4$([C,N]([CH2][CH2][C,N]1)([CH2][CH2]1))]"),
    Chem.MolFromSmarts("[Ax4$([C,N]([CH2][C,N]1)([CH2]1))]"),
)


BRIDGEHEAD_SMARTS_FILTER = Chem.MolFromSmarts("[Ax3,x4]")
SUPPORTED_ATOM_STEREO_LABELS: frozenset[str] = frozenset({"?", "R", "S"})
PSEUDOASYMMETRIC_ATOM_STEREO_LABELS: frozenset[str] = frozenset({"r", "s"})


@dataclass(frozen=True)
class MoleculeStereoSpecification:
    """Specification of atom stereocenters in a molecule.

    :param assigned_atom_centers: Atom indices of assigned atom stereocenters
    :param unassigned_atom_centers: Atom indices of unassigned atomstereocenters
    :param assigned_bridgehead_atom_centers: Atom indices of assigned bridgehead
        atom stereocenters
    :param unassigned_bridgehead_atom_centers: Atom indices of unassigned bridgehead
        atom stereocenters
    :param pseudoasymmetric_atom_centers: Atom indices of pseudoasymmetric
        non-bridgehead stereocenters with lowercase ``r/s`` labels
    :param pseudoasymmetric_bridgehead_atom_centers: Atom indices of
        pseudoasymmetric bridgehead stereocenters with lowercase ``r/s`` labels
    :param atom_center_labels: CIP labels for ordinary (``?``/``R``/``S``) and
        pseudoasymmetric (``r``/``s``) atom stereocenters. Atom indices are keys.
    :type atom_center_labels: frozendict[int, str]

    :param assigned_bond_centers: Atom indices of assigned bond stereocenters
        Tuples of atom indices of the bond's begin and end atoms.
    :type assigned_bond_centers: tuple[tuple[int, int], ...]
    :param unassigned_bond_centers: Atom indices of unassigned bond stereocenters
        Tuples of atom indices of the bond's begin and end atoms.

    """

    assigned_atom_centers: tuple[int, ...]
    unassigned_atom_centers: tuple[int, ...]
    assigned_bridgehead_atom_centers: tuple[int, ...]
    unassigned_bridgehead_atom_centers: tuple[int, ...]
    pseudoasymmetric_atom_centers: tuple[int, ...] = ()
    pseudoasymmetric_bridgehead_atom_centers: tuple[int, ...] = ()
    assigned_bond_centers: tuple[tuple[int, int], ...] = ()
    unassigned_bond_centers: tuple[tuple[int, int], ...] = ()
    atom_center_labels: frozendict[int, str] = frozendict()

    @classmethod
    @lru_cache(maxsize=512)
    def extract_from_molecule(cls, m: Chem.Mol) -> MoleculeStereoSpecification | None:
        """Extract the stereo specification from a molecule.

        :param m: Molecule
        :type m: Chem.Mol
        :return: MoleculeStereoSpecification
        :rtype: MoleculeStereoSpecification | None
        """
        try:
            r_s = Chem.FindMolChiralCenters(
                mol=m,
                includeUnassigned=True,
                useLegacyImplementation=False,
                includeCIP=True,
            )
        except RuntimeError as e:
            raise MoleculeStereoSpecificationRuntimeError(
                msg=str(e), molecule_smiles=Chem.MolToSmiles(m)
            ) from e

        # avoid pseudo-chiral atoms including atoms with attached metals (Li, Na, K)
        # and pseudo-bridgehead atoms
        avoid_atoms: set[int] = {
            match[0]
            for avoid_atoms_filter in PSEUDO_CHIRAL_ATOMS_SMARTS_FILTERS
            for match in m.GetSubstructMatches(avoid_atoms_filter)
        }

        bridgehead_atoms: set[int] = {
            match[0] for match in m.GetSubstructMatches(BRIDGEHEAD_SMARTS_FILTER)
        }

        filtered_r_s = [center for center in r_s if center[0] not in avoid_atoms]
        supported_r_s = [
            center
            for center in filtered_r_s
            if center[1] in SUPPORTED_ATOM_STEREO_LABELS
        ]
        pseudo_r_s = [
            center
            for center in filtered_r_s
            if center[1] in PSEUDOASYMMETRIC_ATOM_STEREO_LABELS
        ]

        # Non bridgehead atoms
        non_bridgehead_atoms = set(
            center for center in supported_r_s if center[0] not in bridgehead_atoms
        )
        assigned_atoms = set(center for center in supported_r_s if center[1] != "?")

        assigned_non_bridgehead_atoms = assigned_atoms & non_bridgehead_atoms
        assigned_atom_centers = tuple(
            center[0] for center in assigned_non_bridgehead_atoms
        )

        unassigned_non_bridgehead_atoms = non_bridgehead_atoms - assigned_atoms
        unassigned_atom_centers = tuple(
            center[0] for center in unassigned_non_bridgehead_atoms
        )
        pseudoasymmetric_atom_centers = tuple(
            center[0] for center in pseudo_r_s if center[0] not in bridgehead_atoms
        )

        # Bridgehead atoms
        bridgehead_centers = set(supported_r_s) - non_bridgehead_atoms
        assigned_bridgehead_atoms = assigned_atoms & bridgehead_centers
        assigned_bridgehead_atom_centers = tuple(
            center[0] for center in assigned_bridgehead_atoms
        )

        unassigned_bridgehead_atoms = bridgehead_centers - assigned_atoms
        unassigned_bridgehead_atom_centers = tuple(
            center[0] for center in unassigned_bridgehead_atoms
        )
        pseudoasymmetric_bridgehead_atom_centers = tuple(
            center[0] for center in pseudo_r_s if center[0] in bridgehead_atoms
        )

        atom_center_labels = frozendict(
            {atom_idx: label for atom_idx, label in supported_r_s}
            | {atom_idx: label for atom_idx, label in pseudo_r_s}
        )

        m_generated_iso = None
        assigned_bond_centers = []
        unassigned_bond_centers = []

        for b in m.GetBonds():
            # we are interested only in double bonds
            if b.GetBondType() != Chem.BondType.DOUBLE:
                continue

            if b.GetStereo() != Chem.BondStereo.STEREONONE:
                assigned_bond_centers.append((b.GetBeginAtomIdx(), b.GetEndAtomIdx()))
            else:
                if m_generated_iso is None:
                    opts = StereoEnumerationOptions(maxIsomers=1)
                    m_generated_iso = tuple(EnumerateStereoisomers(m, options=opts))[0]

                new_stereo = m_generated_iso.GetBondWithIdx(b.GetIdx()).GetStereo()
                if new_stereo != Chem.BondStereo.STEREONONE:
                    unassigned_bond_centers.append(
                        (b.GetBeginAtomIdx(), b.GetEndAtomIdx())
                    )

        return cls(
            assigned_atom_centers=assigned_atom_centers,
            unassigned_atom_centers=unassigned_atom_centers,
            assigned_bridgehead_atom_centers=assigned_bridgehead_atom_centers,
            unassigned_bridgehead_atom_centers=unassigned_bridgehead_atom_centers,
            pseudoasymmetric_atom_centers=pseudoasymmetric_atom_centers,
            pseudoasymmetric_bridgehead_atom_centers=(
                pseudoasymmetric_bridgehead_atom_centers
            ),
            atom_center_labels=atom_center_labels,
            assigned_bond_centers=tuple(assigned_bond_centers),
            unassigned_bond_centers=tuple(unassigned_bond_centers),
        )


def collect_stereo_centers(
    stereo_spec: MoleculeStereoSpecification,
) -> tuple[set[int], set[int]]:
    """Collect assigned and unassigned centers (atoms).

    :param stereo_spec: MoleculeStereoSpecification
    :type stereo_spec: MoleculeStereoSpecification
    :return: tuple of sets of assigned and unassigned atom indices
    :rtype: tuple[set[int], set[int]]
    """
    assigned_atoms = set(stereo_spec.assigned_atom_centers) | set(
        stereo_spec.assigned_bridgehead_atom_centers
    )

    unassigned_atoms = set(stereo_spec.unassigned_atom_centers) | set(
        stereo_spec.unassigned_bridgehead_atom_centers
    )

    return assigned_atoms, unassigned_atoms


def collect_pseudoasymmetric_centers(
    stereo_spec: MoleculeStereoSpecification,
) -> set[int]:
    """Collect pseudoasymmetric atom centers with lowercase ``r/s`` labels.

    :param stereo_spec: MoleculeStereoSpecification
    :type stereo_spec: MoleculeStereoSpecification
    :return: set of pseudoasymmetric atom indices
    :rtype: set[int]
    """
    return set(stereo_spec.pseudoasymmetric_atom_centers) | set(
        stereo_spec.pseudoasymmetric_bridgehead_atom_centers
    )
