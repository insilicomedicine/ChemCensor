from rdkit import Chem

from chemcensor.basic import Molecule
from chemcensor.basic import MoleculeStereoSpecification
from chemcensor.basic.molecule_stereo_specification import (
    collect_pseudoasymmetric_centers,
)
from chemcensor.basic.molecule_stereo_specification import collect_stereo_centers


def _mol(smiles: str) -> Chem.Mol:
    """Create an RDKit Mol from SMILES."""
    mol = Molecule.from_atom_mapped_smiles(smiles)
    return mol.canonical_rdmol


# ============================================================================
# extract_from_molecule — no stereocenters
# ============================================================================


def test_simple_achiral():
    spec = MoleculeStereoSpecification.extract_from_molecule(_mol("CCCC"))
    assert spec.assigned_atom_centers == ()
    assert spec.unassigned_atom_centers == ()
    assert spec.assigned_bridgehead_atom_centers == ()
    assert spec.unassigned_bridgehead_atom_centers == ()


def test_symmetric_molecule():
    spec = MoleculeStereoSpecification.extract_from_molecule(_mol("CC1CCCCC1"))
    assert spec.assigned_atom_centers == ()
    assert spec.unassigned_atom_centers == ()
    assert spec.assigned_bridgehead_atom_centers == ()
    assert spec.unassigned_bridgehead_atom_centers == ()


# ============================================================================
# extract_from_molecule — assigned stereocenters
# ============================================================================


def test_single_assigned_center():
    spec = MoleculeStereoSpecification.extract_from_molecule(_mol("C[C@H](O)F"))
    assert len(spec.assigned_atom_centers) == 1
    assert spec.unassigned_atom_centers == ()


def test_two_assigned_centers():
    spec = MoleculeStereoSpecification.extract_from_molecule(
        _mol("F[C@@H](Cl)[C@H](Br)I")
    )
    assert len(spec.assigned_atom_centers) == 2
    assert spec.unassigned_atom_centers == ()


# ============================================================================
# extract_from_molecule — unassigned stereocenters
# ============================================================================


def test_single_unassigned_center():
    spec = MoleculeStereoSpecification.extract_from_molecule(_mol("CC(O)F"))
    assert spec.assigned_atom_centers == ()
    assert len(spec.unassigned_atom_centers) == 1


def test_two_unassigned_centers():
    spec = MoleculeStereoSpecification.extract_from_molecule(_mol("FC(Cl)C(Br)I"))
    assert spec.assigned_atom_centers == ()
    assert len(spec.unassigned_atom_centers) == 2


# ============================================================================
# extract_from_molecule — mixed assigned / unassigned
# ============================================================================


def test_one_assigned_one_unassigned():
    spec = MoleculeStereoSpecification.extract_from_molecule(_mol("F[C@@H](Cl)C(Br)I"))
    assert len(spec.assigned_atom_centers) == 1
    assert len(spec.unassigned_atom_centers) == 1


# ============================================================================
# extract_from_molecule — pseudo-chiral filtering
# ============================================================================


def test_pseudo_chiral_filtering():
    spec = MoleculeStereoSpecification.extract_from_molecule(
        _mol("CC([C@H]1CN2CCC1CC2)=O")
    )
    assert len(spec.assigned_atom_centers) == 1
    assert len(spec.unassigned_atom_centers) == 0
    assert spec.assigned_bridgehead_atom_centers == ()
    assert spec.unassigned_bridgehead_atom_centers == ()
    spec2 = MoleculeStereoSpecification.extract_from_molecule(
        _mol("N[C@H]1C(C2)CC2[C@@H]1C(C)=O")
    )
    assert len(spec2.assigned_atom_centers) == 2
    assert len(spec2.unassigned_atom_centers) == 0
    assert spec2.assigned_bridgehead_atom_centers == ()
    assert spec2.unassigned_bridgehead_atom_centers == ()


def test_pseudoasymmetric_r_s_labels_are_in_atom_center_labels():
    spec = MoleculeStereoSpecification.extract_from_molecule(
        _mol("COc1ccc(-n2ncc3c(C4CC4)cc(O[C@@H]4C[C@H](C)C4)nc32)nc1")
    )
    assert spec.assigned_atom_centers == ()
    assert spec.unassigned_atom_centers == ()
    assert spec.assigned_bridgehead_atom_centers == ()
    assert spec.unassigned_bridgehead_atom_centers == ()
    assert len(spec.pseudoasymmetric_atom_centers) == 2
    assert spec.pseudoasymmetric_bridgehead_atom_centers == ()
    assert len(spec.atom_center_labels) == 2
    assert set(spec.atom_center_labels.keys()) == set(
        spec.pseudoasymmetric_atom_centers
    )
    assert set(spec.atom_center_labels.values()) <= {"r", "s"}
    assert collect_pseudoasymmetric_centers(spec) == set(
        spec.pseudoasymmetric_atom_centers
    )


# ============================================================================
# extract_from_molecule — bridgehead atoms
# ============================================================================


def test_bridgehead_atoms():
    spec = MoleculeStereoSpecification.extract_from_molecule(
        _mol("CC([C@H]1CC2CCCC1CC2)=O")
    )
    assert len(spec.assigned_atom_centers) == 1
    assert len(spec.unassigned_atom_centers) == 0
    assert len(spec.assigned_bridgehead_atom_centers) == 0
    assert len(spec.unassigned_bridgehead_atom_centers) == 2
    spec2 = MoleculeStereoSpecification.extract_from_molecule(
        _mol("CC([C@H]1C[C@@H]2CCC[C@H]1CC2)=O")
    )
    assert len(spec2.assigned_atom_centers) == 1
    assert len(spec2.unassigned_atom_centers) == 0
    assert len(spec2.assigned_bridgehead_atom_centers) == 2
    assert len(spec2.unassigned_bridgehead_atom_centers) == 0


# ============================================================================
# collect_stereo_centers
# ============================================================================


def test_empty_spec():
    spec = MoleculeStereoSpecification(
        assigned_atom_centers=(),
        unassigned_atom_centers=(),
        assigned_bridgehead_atom_centers=(),
        unassigned_bridgehead_atom_centers=(),
        assigned_bond_centers=(),
        unassigned_bond_centers=(),
    )
    assigned, unassigned = collect_stereo_centers(spec)
    assert assigned == set()
    assert unassigned == set()


def test_assigned_atoms_only():
    spec = MoleculeStereoSpecification(
        assigned_atom_centers=(1, 3),
        unassigned_atom_centers=(),
        assigned_bridgehead_atom_centers=(),
        unassigned_bridgehead_atom_centers=(),
        assigned_bond_centers=(),
        unassigned_bond_centers=(),
    )
    assigned, unassigned = collect_stereo_centers(spec)
    assert assigned == {1, 3}
    assert unassigned == set()


def test_unassigned_atoms_only():
    spec = MoleculeStereoSpecification(
        assigned_atom_centers=(),
        unassigned_atom_centers=(2, 4),
        assigned_bridgehead_atom_centers=(),
        unassigned_bridgehead_atom_centers=(),
        assigned_bond_centers=(),
        unassigned_bond_centers=(),
    )
    assigned, unassigned = collect_stereo_centers(spec)
    assert assigned == set()
    assert unassigned == {2, 4}


def test_bridgehead_merged_with_regular():
    spec = MoleculeStereoSpecification(
        assigned_atom_centers=(1,),
        unassigned_atom_centers=(2,),
        assigned_bridgehead_atom_centers=(5,),
        unassigned_bridgehead_atom_centers=(6,),
        assigned_bond_centers=(),
        unassigned_bond_centers=(),
    )
    assigned, unassigned = collect_stereo_centers(spec)
    assert assigned == {1, 5}
    assert unassigned == {2, 6}


def test_no_overlap_between_assigned_and_unassigned():
    spec = MoleculeStereoSpecification(
        assigned_atom_centers=(1, 3),
        unassigned_atom_centers=(2, 4),
        assigned_bridgehead_atom_centers=(5,),
        unassigned_bridgehead_atom_centers=(6,),
        assigned_bond_centers=(),
        unassigned_bond_centers=(),
    )
    assigned, unassigned = collect_stereo_centers(spec)
    assert assigned & unassigned == set()
