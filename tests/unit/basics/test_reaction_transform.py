import pytest
from frozendict import frozendict

from chemcensor.basic.errors.molecule_errors import InvalidSMILESError
from chemcensor.basic.errors.reaction_transform_errors import ProductMissingAtomMapError
from chemcensor.basic.errors.reaction_transform_errors import (
    ReactantsMissingAtomMapError,
)
from chemcensor.basic.molecule import Molecule
from chemcensor.basic.reaction_transform import ReactionTransform


@pytest.fixture
def simple_reaction_smiles() -> str:
    """Simple reaction SMILES with atom mapping."""
    return "[CH3:1][OH:2]>>[CH3:1][O-:2]"


@pytest.fixture
def sear_reaction_smiles() -> str:
    """SEAr reaction SMILES example."""
    return (
        "[F:8][C:5]([F:6])([F:7])[c:4]1[cH:3][cH:2][c:11]([Cl:12])"
        "[cH:10][n:9]1.[Li+:1]>>[Li:1][c:2]1[cH:3][c:4]([C:5]([F:6])"
        "([F:7])[F:8])[n:9][cH:10][c:11]1[Cl:12]"
    )


@pytest.fixture
def non_sear_reaction_smiles() -> str:
    """Non-SEAr reaction SMILES example."""
    return (
        "[CH3:1][C:2]([CH3:3])([OH:4])[c:5]1[cH:6][c:7]([C:8]([F:9])"
        "([F:10])[F:11])[n:12][cH:13][c:14]1-[c:15]1[cH:16][cH:17]"
        "[c:18]([C:19]2([C:20]#N)[CH2:23][O:24][CH2:25]2)[cH:26]"
        "[cH:27]1.[OH-:21].[OH2:22]>>[CH3:1][C:2]([CH3:3])([OH:4])"
        "[c:5]1[cH:6][c:7]([C:8]([F:9])([F:10])[F:11])[n:12][cH:13]"
        "[c:14]1-[c:15]1[cH:16][cH:17][c:18]([C:19]2([C:20](=[O:21])"
        "[OH:22])[CH2:23][O:24][CH2:25]2)[cH:26][cH:27]1"
    )


@pytest.fixture
def reaction_with_missing_product_atom_map() -> str:
    """Reaction with missing product atom map."""
    return "[CH3:1][OH:2]>>C(=O)O"


@pytest.fixture
def reaction_with_missing_reactants_atom_maps() -> str:
    """Reaction with missing reactants atom maps."""
    return "C(=O)O>>[CH3:1][OH:2]"


@pytest.fixture
def reaction_without_changing_atoms() -> str:
    """Reaction without changing atoms."""
    return "[CH3:1][OH:2]>>[CH3:1][OH:2]"


@pytest.fixture
def simple_transform(simple_reaction_smiles: str) -> ReactionTransform:
    """Create a simple ReactionTransform."""
    return ReactionTransform.from_reaction_smiles(simple_reaction_smiles)


def test_reaction_without_changing_atoms_transform(
    reaction_without_changing_atoms: str,
):
    """Create a reaction without changing atoms transform."""
    transform = ReactionTransform.from_reaction_smiles(reaction_without_changing_atoms)
    # When no atoms change, reacting atoms should be empty tuples, not None
    assert transform.p_reacting_atoms == ()
    assert transform.R_reacting_atoms == ((),)


def test_reaction_transform_from_reaction_smiles(simple_reaction_smiles: str):
    """Test creating ReactionTransform from reaction SMILES."""
    transform = ReactionTransform.from_reaction_smiles(simple_reaction_smiles)
    assert transform is not None
    assert isinstance(transform, ReactionTransform)


def test_reaction_transform_has_reactants(simple_transform: ReactionTransform):
    """Test that transform has reactants."""
    assert simple_transform.reactants is not None
    assert isinstance(simple_transform.reactants, tuple)
    assert len(simple_transform.reactants) == 1
    assert all(isinstance(r, Molecule) for r in simple_transform.reactants)


def test_reaction_transform_has_product(simple_transform: ReactionTransform):
    """Test that transform has product."""
    assert simple_transform.product is not None
    assert isinstance(simple_transform.product, Molecule)


def test_reaction_transform_pR_map(simple_transform: ReactionTransform):
    """Test product-to-reactant mapping."""
    assert simple_transform.pR_map is not None
    assert isinstance(simple_transform.pR_map, frozendict)
    # Each product atom should map to (reactant_idx, atom_idx) or None
    for p_idx, mapping in simple_transform.pR_map.items():
        assert isinstance(p_idx, int)
        assert mapping is None or (isinstance(mapping, tuple) and len(mapping) == 2)


def test_reaction_transform_Rp_map(simple_transform: ReactionTransform):
    """Test reactant-to-product mapping."""
    assert simple_transform.Rp_map is not None
    assert isinstance(simple_transform.Rp_map, tuple)
    assert len(simple_transform.Rp_map) == len(simple_transform.reactants)
    # Each reactant should have a mapping to product
    for rp_map in simple_transform.Rp_map:
        assert isinstance(rp_map, frozendict)


def test_reaction_transform_reacting_atoms(simple_transform: ReactionTransform):
    """Test that reacting atoms are identified."""
    # Product reacting atoms
    assert simple_transform.p_reacting_atoms is not None
    assert isinstance(simple_transform.p_reacting_atoms, tuple)

    # Reactant reacting atoms
    assert simple_transform.R_reacting_atoms is not None
    assert isinstance(simple_transform.R_reacting_atoms, tuple)
    assert len(simple_transform.R_reacting_atoms) == len(simple_transform.reactants)


def test_reaction_transform_with_multiple_reactants(sear_reaction_smiles: str):
    """Test transform with multiple reactants."""
    transform = ReactionTransform.from_reaction_smiles(sear_reaction_smiles)
    assert len(transform.reactants) == 2
    assert len(transform.Rp_map) == 2
    assert transform.R_reacting_atoms is not None
    assert len(transform.R_reacting_atoms) == 2


def test_reaction_transform_complex_reaction(non_sear_reaction_smiles: str):
    """Test transform with complex reaction."""
    transform = ReactionTransform.from_reaction_smiles(non_sear_reaction_smiles)
    # This reaction has 3 reactants
    assert len(transform.reactants) == 3
    assert transform.product is not None
    assert transform.p_reacting_atoms is not None
    assert transform.R_reacting_atoms is not None
    assert len(transform.R_reacting_atoms) == 3


def test_reaction_transform_handles_unmapped_smiles():
    """Test that transform rejects SMILES without explicit atom mapping."""
    smiles_no_map = "CO>>CO"
    with pytest.raises(ProductMissingAtomMapError):
        ReactionTransform.from_reaction_smiles(smiles_no_map)


def test_reaction_transform_invalid_smiles():
    """Test that invalid SMILES raises an error."""
    invalid_smiles = "invalid>>invalid"
    # Should raise AttributeError because Molecule will be invalid
    with pytest.raises(InvalidSMILESError):
        ReactionTransform.from_reaction_smiles(invalid_smiles)


def test_reaction_transform_frozen(simple_transform: ReactionTransform):
    """Test that ReactionTransform is immutable (frozen)."""
    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        simple_transform.reactants = ()  # type: ignore


def test_reaction_transform_fields_are_immutable(
    simple_transform: ReactionTransform,
):
    """Test that all mapping fields are immutable."""
    assert isinstance(simple_transform.pR_map, frozendict)
    assert isinstance(simple_transform.Rp_map, tuple)
    for rp_map in simple_transform.Rp_map:
        assert isinstance(rp_map, frozendict)
    assert isinstance(simple_transform.reactants, tuple)
    assert isinstance(simple_transform.p_reacting_atoms, tuple)
    assert isinstance(simple_transform.R_reacting_atoms, tuple)


def test_reaction_transform_mapping_consistency(
    simple_transform: ReactionTransform,
):
    """Test that pR_map and Rp_map are consistent."""
    # For each product atom mapped to reactant
    for p_idx, pr_mapping in simple_transform.pR_map.items():
        if pr_mapping is not None:
            r_idx, r_atom_idx = pr_mapping
            # Check reverse mapping exists
            rp_map = simple_transform.Rp_map[r_idx]
            assert r_atom_idx in rp_map
            # Reverse mapping should point back to product atom
            assert rp_map[r_atom_idx] == p_idx


def test_reaction_transform_reacting_atoms_in_product(
    simple_transform: ReactionTransform,
):
    """Test that reacting atoms are within product atom range."""
    assert simple_transform.p_reacting_atoms is not None
    for p_atom_idx in simple_transform.p_reacting_atoms:
        assert 0 <= p_atom_idx < simple_transform.product.num_atoms


def test_reaction_transform_reacting_atoms_in_reactants(
    simple_transform: ReactionTransform,
):
    """Test that reacting atoms are within reactant atom ranges."""
    assert simple_transform.R_reacting_atoms is not None
    for r_idx, r_reacting_atoms in enumerate(simple_transform.R_reacting_atoms):
        reactant = simple_transform.reactants[r_idx]
        for r_atom_idx in r_reacting_atoms:
            assert 0 <= r_atom_idx < reactant.num_atoms


def test_reaction_transform_sear_reaction_structure(
    sear_reaction_smiles: str,
):
    """Test structure of SEAr reaction transform."""
    transform = ReactionTransform.from_reaction_smiles(sear_reaction_smiles)
    # SEAr reaction: 2 reactants -> 1 product
    assert len(transform.reactants) == 2
    assert transform.product.num_atoms > 0
    # Should have reacting atoms identified
    assert transform.p_reacting_atoms is not None
    assert len(transform.p_reacting_atoms) > 0


def test_reaction_transform_atom_map_coverage(
    simple_transform: ReactionTransform,
):
    """Test that all product atoms are either mapped or new."""
    # Every product atom should be in pR_map
    for p_idx in range(simple_transform.product.num_atoms):
        assert p_idx in simple_transform.pR_map


def test_reaction_transform_from_reaction_smiles_splits_correctly():
    """Test that reaction SMILES is split correctly."""
    reaction = "[C:1].[N:2]>>[C:1][N:2]"
    transform = ReactionTransform.from_reaction_smiles(reaction)
    # Should have 2 reactants
    assert len(transform.reactants) == 2


def test_reaction_transform_reactants_are_molecules(
    simple_transform: ReactionTransform,
):
    """Test that all reactants are valid Molecule objects."""
    for reactant in simple_transform.reactants:
        assert isinstance(reactant, Molecule)
        assert reactant.canonical_smiles is not None


def test_reaction_transform_product_is_molecule(
    simple_transform: ReactionTransform,
):
    """Test that product is a valid Molecule object."""
    assert isinstance(simple_transform.product, Molecule)
    assert simple_transform.product.canonical_smiles is not None


def test_reaction_transform_repr(simple_transform: ReactionTransform):
    """Test that transform has reasonable repr."""
    repr_str = repr(simple_transform)
    assert "ReactionTransform" in repr_str


def test_reacting_atoms_detection(simple_transform: ReactionTransform):
    """Test that reacting atoms are detected correctly."""
    assert simple_transform.p_reacting_atoms is not None
    assert simple_transform.R_reacting_atoms is not None
    p_reacting_set = set(simple_transform.p_reacting_atoms)
    for p_atom_idx in simple_transform.p_reacting_atoms:
        assert p_atom_idx in simple_transform.pR_map
    for r_idx, r_reacting_atoms in enumerate(simple_transform.R_reacting_atoms):
        for r_atom_idx in r_reacting_atoms:
            assert r_atom_idx in simple_transform.Rp_map[r_idx]
            mapped_p_idx = simple_transform.Rp_map[r_idx][r_atom_idx]
            # reacting reactant atom maps to a reacting product atom or is unmapped
            assert mapped_p_idx is None or mapped_p_idx in p_reacting_set


@pytest.fixture
def bond_swap_reaction_smiles() -> str:
    """Acylation reaction where atom :17 simultaneously loses a bond
    (to unmapped O) and gains a bond (to :16).  Neither neighbour set
    is a strict subset of the other — this must still be detected as a
    reacting atom."""
    return (
        "[CH3:1][O:2][C:3](=[O:4])[c:5]1[cH:6][cH:7][cH:8][cH:9]"
        "[c:10]1-[c:11]1[cH:12][cH:13][c:14]([CH2:15][NH:16]"
        "[C@@H:20]2[CH2:21][CH2:22][CH2:23][CH:24]2[N:25]"
        "([CH2:26][C:27]([F:28])([F:29])[F:30])[C:31]([CH3:32])"
        "=[O:33])[nH:34]1.[CH3:18][C:17](=[O:19])OC(C)=O>>"
        "[CH3:1][O:2][C:3](=[O:4])[c:5]1[cH:6][cH:7][cH:8][cH:9]"
        "[c:10]1-[c:11]1[cH:12][cH:13][c:14]([CH2:15][N:16]"
        "([C:17]([CH3:18])=[O:19])[C@@H:20]2[CH2:21][CH2:22]"
        "[CH2:23][CH:24]2[N:25]([CH2:26][C:27]([F:28])([F:29])"
        "[F:30])[C:31]([CH3:32])=[O:33])[nH:34]1"
    )


def test_bond_swap_detects_both_reacting_atoms(
    bond_swap_reaction_smiles: str,
) -> None:
    """Atom :17 swaps a bond (loses unmapped O, gains :16).

    Both :16 and :17 must appear in ``p_reacting_atoms`` so that
    neighbour-depth expansion covers the full reaction centre.
    """
    T = ReactionTransform.from_reaction_smiles(bond_swap_reaction_smiles)
    p_map = T.product.atom_map
    assert p_map is not None

    # canonical indices for atom-map numbers 16 and 17
    idx_16 = next(k for k, v in p_map.items() if v == 16)
    idx_17 = next(k for k, v in p_map.items() if v == 17)

    assert T.p_reacting_atoms is not None
    assert idx_16 in T.p_reacting_atoms, "atom :16 (N) must be reacting"
    assert idx_17 in T.p_reacting_atoms, "atom :17 (C) must be reacting (bond swap)"


def test_reaction_transform_with_missing_product_atom_map(
    reaction_with_missing_product_atom_map: str,
):
    """Test that reaction transform raises an error when
    product has missing atom map."""
    with pytest.raises(ProductMissingAtomMapError):
        ReactionTransform.from_reaction_smiles(reaction_with_missing_product_atom_map)


def test_reaction_transform_with_missing_reactants_atom_maps(
    reaction_with_missing_reactants_atom_maps: str,
):
    """Test that reaction transform raises an error when
    reactants have missing atom maps."""
    with pytest.raises(ReactantsMissingAtomMapError):
        ReactionTransform.from_reaction_smiles(
            reaction_with_missing_reactants_atom_maps
        )
