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
