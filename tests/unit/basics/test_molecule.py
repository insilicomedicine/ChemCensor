import pytest
from frozendict import frozendict
from rdkit import Chem

from chemcensor.basic.errors.molecule_errors import InvalidSMILESError
from chemcensor.basic.molecule import Molecule


@pytest.fixture
def simple_smiles() -> str:
    """Simple SMILES for benzene."""
    return "c1ccccc1"


@pytest.fixture
def mapped_smiles() -> str:
    """Atom-mapped SMILES for a simple molecule."""
    return "[CH3:1][CH2:2][OH:3]"


@pytest.fixture
def benzene_molecule(simple_smiles: str) -> Molecule:
    """Create a benzene molecule."""
    return Molecule(simple_smiles)


def test_molecule_from_smiles(simple_smiles: str):
    """Test creating molecule from SMILES string."""
    mol = Molecule(simple_smiles)
    assert mol.canonical_smiles == "c1ccccc1"
    assert mol.canonical_rdmol is not None
    assert mol.num_atoms == 6


def test_molecule_invalid_input():
    """Test that invalid input raises InvalidSMILESError."""
    with pytest.raises(InvalidSMILESError, match="Invalid SMILES string"):
        Molecule("123")


def test_molecule_invalid_smiles():
    """Test handling of invalid SMILES."""
    with pytest.raises(InvalidSMILESError, match="Invalid SMILES string"):
        _ = Molecule("invalid_smiles_xyz")


def test_molecule_atom_map_default(benzene_molecule: Molecule):
    """Test that default atom map is created."""
    assert benzene_molecule.atom_map is not None
    assert len(benzene_molecule.atom_map) == 6
    # Default atom map: {0: 1, 1: 2, ..., 5: 6}
    for i in range(6):
        assert benzene_molecule.atom_map[i] == i + 1


def test_molecule_atom_map_disabled():
    """Test creating molecule with disabled atom map."""
    mol = Molecule("c1ccccc1", disable_internal_atom_map=True)
    assert mol.atom_map is None


def test_molecule_atom_map_from_dict():
    """Test creating molecule with custom atom map."""
    custom_map = frozendict({0: 10, 1: 20, 2: 30})
    mol = Molecule("CCC", atom_map_from_dict=custom_map)
    assert mol.atom_map is not None
    assert 10 in mol.atom_map.values()
    assert 20 in mol.atom_map.values()
    assert 30 in mol.atom_map.values()


def test_molecule_from_atom_mapped_smiles(mapped_smiles: str):
    """Test creating molecule from atom-mapped SMILES."""
    mol = Molecule(mapped_smiles)
    assert mol.canonical_smiles is not None
    assert mol.num_atoms == 3
    assert mol.atom_map is not None


def test_molecule_canonical_smiles():
    """Test that canonical SMILES is consistent."""
    mol1 = Molecule("C1=CC=CC=C1")  # Benzene notation 1
    mol2 = Molecule("c1ccccc1")  # Benzene notation 2
    assert mol1 == mol2


def test_molecule_atom_mapped_canonical_smiles(benzene_molecule: Molecule):
    """Test atom-mapped canonical SMILES generation."""
    assert benzene_molecule.atom_mapped_canonical_smiles is not None
    assert isinstance(benzene_molecule.atom_mapped_canonical_smiles, str)


def test_molecule_atom_mapped_canonical_rdmol(benzene_molecule: Molecule):
    """Test atom-mapped canonical RDKit Mol generation."""
    assert benzene_molecule.atom_mapped_canonical_rdmol is not None
    assert isinstance(benzene_molecule.atom_mapped_canonical_rdmol, Chem.Mol)


def test_molecule_equality():
    """Test molecule equality based on canonical SMILES."""
    mol1 = Molecule("C1=CC=CC=C1")
    mol2 = Molecule("c1ccccc1")
    mol3 = Molecule("CCCCCC")  # Hexane, different molecule
    assert mol1 == mol2
    assert mol1 != mol3
    assert mol2 != mol3


def test_molecule_hash():
    """Test that molecules with same canonical SMILES have same hash."""
    mol1 = Molecule("C1=CC=CC=C1")
    mol2 = Molecule("c1ccccc1")
    mol3 = Molecule("CCCCCC")
    assert hash(mol1) == hash(mol2)
    assert hash(mol1) != hash(mol3)


def test_molecule_can_be_used_in_set():
    """Test that molecules can be used in sets."""
    mol1 = Molecule("c1ccccc1")
    mol2 = Molecule("C1=CC=CC=C1")  # Same as mol1
    mol3 = Molecule("CCCCCC")
    molecule_set = {mol1, mol2, mol3}
    # mol1 and mol2 are the same, so set should have 2 elements
    assert len(molecule_set) == 2


def test_molecule_can_be_used_in_dict():
    """Test that molecules can be used as dictionary keys."""
    mol1 = Molecule("c1ccccc1")
    mol2 = Molecule("C1=CC=CC=C1")  # Same as mol1
    mol3 = Molecule("CCCCCC")
    molecule_dict = {mol1: "benzene", mol3: "hexane"}
    # mol2 should access the same value as mol1
    assert molecule_dict[mol2] == "benzene"
    assert len(molecule_dict) == 2


def test_molecule_frozen():
    """Test that molecule is immutable (frozen)."""
    mol = Molecule("c1ccccc1")
    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        mol.canonical_smiles = "new_value"  # type: ignore


def test_molecule_fields_are_immutable():
    """Test that all fields use immutable types."""
    mol = Molecule("CCC")
    # atom_map should be frozendict
    assert isinstance(mol.atom_map, frozendict)


def test_molecule_with_complex_structure():
    """Test molecule with complex structure."""
    # Aspirin SMILES
    aspirin_smiles = "CC(=O)Oc1ccccc1C(=O)O"
    mol = Molecule(aspirin_smiles)
    assert mol.num_atoms == 13
    assert mol.canonical_smiles == "CC(=O)Oc1ccccc1C(=O)O"


def test_molecule_repr():
    """Test that molecule has reasonable repr."""
    mol = Molecule("CCC")
    repr_str = repr(mol)
    assert "Molecule" in repr_str


def test_from_atom_mapped_smiles_with_full_mapping():
    """Test from_atom_mapped_smiles with complete atom mapping."""
    # Ethanol with all atoms mapped
    smiles = "[CH3:1][CH2:2][OH:3]"
    mol = Molecule.from_atom_mapped_smiles(smiles)

    assert mol.canonical_smiles is not None
    assert mol.num_atoms == 3
    assert mol.atom_map is not None
    assert len(mol.atom_map) == 3
    # Verify that atom mappings are preserved
    assert 1 in mol.atom_map.values()
    assert 2 in mol.atom_map.values()
    assert 3 in mol.atom_map.values()


def test_from_atom_mapped_smiles_no_mapping():
    """Test from_atom_mapped_smiles without any atom mapping."""
    # Propane without atom mapping
    smiles = "CCC"
    mol = Molecule.from_atom_mapped_smiles(smiles)

    assert mol.canonical_smiles == "CCC"
    assert mol.num_atoms == 3
    # When no mapping is provided, atom_map should still be created
    # but will be None for unmapped atoms
    assert mol.atom_map is not None


def test_from_atom_mapped_smiles_partial_mapping():
    """Test from_atom_mapped_smiles with partial atom mapping."""
    # Benzene with only some atoms mapped
    smiles = "[c:100]1[c:201]cccc1"
    mol = Molecule.from_atom_mapped_smiles(smiles)

    assert mol.num_atoms == 6
    assert mol.atom_map is not None
    # Mapped atoms should have their mappings preserved
    assert 100 in mol.atom_map.values()
    assert 201 in mol.atom_map.values()


def test_from_atom_mapped_smiles_sparse_mapping():
    """Test from_atom_mapped_smiles with non-sequential mapping."""
    # Molecule with sparse/non-sequential atom map numbers
    smiles = "[CH3:10][CH2:20][CH2:30][CH3:40]"
    mol = Molecule.from_atom_mapped_smiles(smiles)

    assert mol.canonical_smiles == "CCCC"
    assert mol.num_atoms == 4
    assert mol.atom_map is not None
    # Verify sparse mappings are preserved
    assert 10 in mol.atom_map.values()
    assert 20 in mol.atom_map.values()
    assert 30 in mol.atom_map.values()
    assert 40 in mol.atom_map.values()


def test_from_atom_mapped_smiles_cyclic_molecule():
    """Test from_atom_mapped_smiles with cyclic molecule."""
    # Cyclohexane with atom mapping
    smiles = "[CH2:1]1[CH2:2][CH2:3][CH2:4][CH2:5][CH2:6]1"
    mol = Molecule.from_atom_mapped_smiles(smiles)

    assert mol.num_atoms == 6
    assert mol.atom_map is not None
    assert len(mol.atom_map) == 6
    # Verify all mappings from 1 to 6 are present
    for i in range(1, 7):
        assert i in mol.atom_map.values()


def test_from_atom_mapped_smiles_complex_molecule():
    """Test from_atom_mapped_smiles with complex structure."""
    # More complex molecule from user's dev.ipynb
    smiles = "C1CC(C(C1)C(C)C)C(C)[CH3:100]"
    mol = Molecule.from_atom_mapped_smiles(smiles)

    assert mol.canonical_smiles is not None
    assert mol.num_atoms > 0
    assert mol.atom_map is not None
    # Verify that the high mapping number is preserved
    assert 100 in mol.atom_map.values()


def test_from_atom_mapped_smiles_preserves_canonicalization():
    """Test that from_atom_mapped_smiles produces same canonical form."""
    # Two different representations of the same molecule
    smiles1 = "[CH3:1][CH2:2][OH:3]"
    smiles2 = "[OH:3][CH2:2][CH3:1]"

    mol1 = Molecule.from_atom_mapped_smiles(smiles1)
    mol2 = Molecule.from_atom_mapped_smiles(smiles2)

    # Should produce the same canonical SMILES
    assert mol1.canonical_smiles == mol2.canonical_smiles
    # Both molecules should be equal
    assert mol1 == mol2


def test_from_atom_mapped_smiles_invalid():
    """Test from_atom_mapped_smiles with invalid SMILES."""
    with pytest.raises(InvalidSMILESError):
        Molecule.from_atom_mapped_smiles("invalid_xyz_123")


def test_molecule_copy():
    """Test molecule copy with custom atom map."""
    mol = Molecule("CCC")
    custom_map = frozendict({0: 10, 1: 20, 2: 30})
    mol_copy = mol.copy(custom_map)

    assert mol_copy.canonical_smiles == mol.canonical_smiles
    assert mol_copy.atom_map == custom_map
    assert mol_copy.atom_map != mol.atom_map


def test_atom_mapped_canonical_smiles_without_atom_map():
    """Test that accessing atom_mapped_canonical_smiles without atom_map
    raises ValueError."""
    mol = Molecule("CCC", disable_internal_atom_map=True)
    with pytest.raises(ValueError, match="Atom map is not set"):
        _ = mol.atom_mapped_canonical_smiles
