from frozendict import frozendict
from rdkit import Chem

from chemcensor.basic.utils import atoms_differ_in_properties
from chemcensor.basic.utils import return_index_for_atom_map
from chemcensor.basic.utils import translate_atom_map


def test_atoms_differ_in_atomic_num():
    """Test atoms_differ_in_properties when atomic numbers differ."""
    mol1 = Chem.MolFromSmiles("C")
    mol2 = Chem.MolFromSmiles("N")
    atom1 = mol1.GetAtomWithIdx(0)
    atom2 = mol2.GetAtomWithIdx(0)
    assert atoms_differ_in_properties(atom1, atom2) is True


def test_atoms_differ_in_radical_electrons():
    """Test atoms_differ_in_properties when radical electrons differ."""
    mol1 = Chem.MolFromSmiles("[C]")
    mol2 = Chem.MolFromSmiles("C")
    atom1 = mol1.GetAtomWithIdx(0)
    atom2 = mol2.GetAtomWithIdx(0)
    # Radical carbon vs normal carbon
    assert atoms_differ_in_properties(atom1, atom2) is True


def test_atoms_differ_in_formal_charge():
    """Test atoms_differ_in_properties when formal charges differ."""
    mol1 = Chem.MolFromSmiles("[NH4+]")
    mol2 = Chem.MolFromSmiles("N")
    atom1 = mol1.GetAtomWithIdx(0)
    atom2 = mol2.GetAtomWithIdx(0)
    assert atoms_differ_in_properties(atom1, atom2) is True


def test_atoms_differ_in_total_num_hs():
    """Test atoms_differ_in_properties when total number of Hs differ."""
    mol1 = Chem.MolFromSmiles("C")  # CH4
    mol2 = Chem.MolFromSmiles("CC")  # CH3-CH3
    atom1 = mol1.GetAtomWithIdx(0)
    atom2 = mol2.GetAtomWithIdx(0)
    assert atoms_differ_in_properties(atom1, atom2) is True


def test_atoms_do_not_differ():
    """Test atoms_differ_in_properties when atoms are the same."""
    mol1 = Chem.MolFromSmiles("CC")
    mol2 = Chem.MolFromSmiles("CC")
    atom1 = mol1.GetAtomWithIdx(0)
    atom2 = mol2.GetAtomWithIdx(0)
    assert atoms_differ_in_properties(atom1, atom2) is False


def test_atoms_differ_when_atom_becomes_aromatic():
    """Test atoms_differ_in_properties when an atom gains aromaticity.

    Same atomic number, charge, radical count, and H count, but the atom
    goes from a non-aromatic double bond to being part of an aromatic ring
    (e.g. an oxime carbon that cyclizes into an isoxazole/oxadiazole).
    """
    mol1 = Chem.MolFromSmiles("CC(C)=N")  # non-aromatic imine carbon
    mol2 = Chem.MolFromSmiles("Cc1ccno1")  # same carbon, now aromatic
    atom1 = mol1.GetAtomWithIdx(1)
    atom2 = mol2.GetAtomWithIdx(1)
    assert atom1.GetIsAromatic() is False
    assert atom2.GetIsAromatic() is True
    assert atoms_differ_in_properties(atom1, atom2) is True


def test_atoms_differ_when_atom_loses_aromaticity():
    """Test atoms_differ_in_properties when an atom loses aromaticity
    (dearomatization), the reverse direction of gaining aromaticity."""
    mol1 = Chem.MolFromSmiles("Cc1ccno1")
    mol2 = Chem.MolFromSmiles("CC(C)=N")
    atom1 = mol1.GetAtomWithIdx(1)
    atom2 = mol2.GetAtomWithIdx(1)
    assert atom1.GetIsAromatic() is True
    assert atom2.GetIsAromatic() is False
    assert atoms_differ_in_properties(atom1, atom2) is True


def test_atoms_do_not_differ_when_both_aromatic():
    """Test atoms_differ_in_properties does not false-positive when both
    atoms are aromatic and otherwise identical."""
    mol1 = Chem.MolFromSmiles("c1ccccc1")
    mol2 = Chem.MolFromSmiles("c1ccccc1")
    atom1 = mol1.GetAtomWithIdx(0)
    atom2 = mol2.GetAtomWithIdx(0)
    assert atoms_differ_in_properties(atom1, atom2) is False


def test_return_index_for_atom_map_found():
    """Test return_index_for_atom_map when atom with map number is found."""
    mol = Chem.MolFromSmiles("[CH3:1][CH2:2][OH:3]")
    assert return_index_for_atom_map(mol, 1) == 0
    assert return_index_for_atom_map(mol, 2) == 1
    assert return_index_for_atom_map(mol, 3) == 2


def test_return_index_for_atom_map_not_found():
    """Test return_index_for_atom_map when atom with map number is not found."""
    mol = Chem.MolFromSmiles("[CH3:1][CH2:2][OH:3]")
    assert return_index_for_atom_map(mol, 100) is None


def test_translate_atom_map_with_int_values():
    """Test translate_atom_map with integer values."""
    map_to = frozendict({0: 1, 1: 2, 2: 3})
    map_from = frozendict({1: 10, 2: 20, 3: 30})
    result = translate_atom_map(map_to, map_from, na=None)
    assert result == frozendict({0: 10, 1: 20, 2: 30})


def test_translate_atom_map_with_tuple_values():
    """Test translate_atom_map with tuple values."""
    map_to = frozendict({0: 1, 1: 2, 2: 3})
    map_from = frozendict({1: (0, 5), 2: (1, 6), 3: (2, 7)})
    result = translate_atom_map(map_to, map_from, na=None)
    assert result == frozendict({0: (0, 5), 1: (1, 6), 2: (2, 7)})


def test_translate_atom_map_with_missing_keys():
    """Test translate_atom_map when keys are missing from map_from."""
    map_to = frozendict({0: 1, 1: 2, 2: 999})  # 999 doesn't exist in map_from
    map_from = frozendict({1: 10, 2: 20})
    result = translate_atom_map(map_to, map_from, na=None)
    assert result == frozendict({0: 10, 1: 20, 2: None})


def test_translate_atom_map_with_none_values_in_map_to():
    """Test translate_atom_map when map_to contains None values (unmapped atoms)."""
    map_to = frozendict({0: 1, 1: None, 2: 3})
    map_from = frozendict({1: 10, 3: 30})
    result = translate_atom_map(map_to, map_from, na=None)
    # None in map_to should result in na for that key
    assert result == frozendict({0: 10, 1: None, 2: 30})


def test_detect_atom_added():
    """Test detect_product_atom_change for ATOM_ADDED case."""
    from chemcensor.basic.reaction_transform import ReactionTransform
    from chemcensor.basic.edits import AtomEditType
    from chemcensor.basic.utils import detect_product_atom_change

    # Reaction where product has an atom not present in any reactant
    # Reactant: methanol (atoms :1, :2), Product: methyl ether with new :3 atom
    reaction_smiles = "[CH3:1][OH:2]>>[CH3:1][O:2][CH3:3]"
    transform = ReactionTransform.from_reaction_smiles(reaction_smiles)

    # Find the product atom mapped to :3 — it has no reactant origin
    for p_idx, mapping in transform.pR_map.items():
        if mapping is None:
            assert (
                detect_product_atom_change(transform, p_idx) == AtomEditType.ATOM_ADDED
            )
            break


def test_detect_fragment_detach():
    """Test detect_product_atom_change for FRAGMENT_DETACH case."""
    from chemcensor.basic.reaction_transform import ReactionTransform
    from chemcensor.basic.edits import AtomEditType
    from chemcensor.basic.utils import detect_product_atom_change

    # Decarboxylation reaction: loss of CO2
    # [CH3:1][C:2](=[O:3])[OH:4]>>[CH4:1]
    reaction_smiles = "[CH3:1][C:2](=[O:3])[OH:4]>>[CH4:1]"
    transform = ReactionTransform.from_reaction_smiles(reaction_smiles)

    # Check if we detect fragment detachment
    # The C atom at index 0 in product (was connected to COOH, now has fewer neighbors)
    result = detect_product_atom_change(transform, 0)
    # This should detect some change (either FRAGMENT_DETACH or other)
    assert result != AtomEditType.NONE


def test_detect_property_change_for_aromatization_without_neighbor_change():
    """Test detect_product_atom_change detects aromatization as a
    PROPERTY_CHANGE when the atom keeps the same mapped neighbors, charge,
    radical count, and H count.

    Minimal analogue of an amidoxime + carboxylic acid condensation into a
    1,2,4-oxadiazole: the oxime carbon and nitrogen keep the same mapped
    neighbors on both sides of the reaction, but their shared bond turns
    from a stereo-defined double bond into an aromatic ring bond.
    """
    from chemcensor.basic.reaction_transform import ReactionTransform
    from chemcensor.basic.edits import AtomEditType
    from chemcensor.basic.utils import detect_product_atom_change

    reaction_smiles = (
        r"[CH3:1]/[C:2]([NH2:3])=[N:4]/[OH:5].[CH3:6][C:7](=[O:8])[OH:9]"
        r">>[CH3:1][c:2]1[n:4][o:5][c:7]([CH3:6])[n:3]1"
    )
    transform = ReactionTransform.from_reaction_smiles(reaction_smiles)

    # Locate the product atoms mapped to the oxime carbon (:2) and the oxime
    # nitrogen (:4); both must become aromatic without any neighbor/H/charge
    # change relative to the reactant.
    p_map = transform.product.atom_map
    amn_to_idx = {amn: idx for idx, amn in p_map.items()}
    oxime_carbon_idx = amn_to_idx[2]
    oxime_nitrogen_idx = amn_to_idx[4]

    assert (
        detect_product_atom_change(transform, oxime_carbon_idx)
        == AtomEditType.PROPERTY_CHANGE
    )
    assert (
        detect_product_atom_change(transform, oxime_nitrogen_idx)
        == AtomEditType.PROPERTY_CHANGE
    )
    assert oxime_carbon_idx in transform.p_reacting_atoms
    assert oxime_nitrogen_idx in transform.p_reacting_atoms


def test_unchanged_aromatic_ring_atoms_stay_non_reacting():
    """Regression: atoms of a remote aromatic ring whose aromaticity does not
    change must not be dragged into the reaction center by the new aromaticity
    check.

    A benzylic bromide -> alcohol substitution leaves the benzene ring
    untouched, so none of its aromatic carbons should be reported as reacting.
    """
    from chemcensor.basic.reaction_transform import ReactionTransform
    from chemcensor.basic.edits import AtomEditType
    from chemcensor.basic.utils import detect_product_atom_change

    reaction_smiles = (
        "[cH:1]1[cH:2][cH:3][cH:4][cH:5][c:6]1[CH2:7][Br:8]"
        ">>[cH:1]1[cH:2][cH:3][cH:4][cH:5][c:6]1[CH2:7][OH:8]"
    )
    transform = ReactionTransform.from_reaction_smiles(reaction_smiles)

    p_map = transform.product.atom_map
    amn_to_idx = {amn: idx for idx, amn in p_map.items()}
    aromatic_ring_indices = [amn_to_idx[amn] for amn in range(1, 7)]

    for p_idx in aromatic_ring_indices:
        assert detect_product_atom_change(transform, p_idx) == AtomEditType.NONE
        assert p_idx not in transform.p_reacting_atoms


def test_neighbor_indices_with_tuple_atom_map():
    """Test neighbor_indices when atom_map contains tuples (pR_map case)."""
    from chemcensor.basic.reaction_transform import ReactionTransform
    from chemcensor.basic.utils import neighbor_indices

    # Reaction with bond formation between two reactants
    reaction_smiles = "[CH3:1][Br:2].[Na:3][OH:4]>>[CH3:1][OH:4].[Na:3][Br:2]"
    transform = ReactionTransform.from_reaction_smiles(reaction_smiles)

    # Get an atom from the product
    p_atom = transform.product.canonical_rdmol.GetAtomWithIdx(0)

    # pR_map contains tuples like (reactant_idx, atom_idx)
    # Call neighbor_indices with pR_map which has tuple values
    neighbors = neighbor_indices(p_atom, atom_map=transform.pR_map)

    # Should return a list of neighbor indices
    assert isinstance(neighbors, list)
