import copy
from collections.abc import Mapping
from typing import TypeVar

import numpy as np
from frozendict import frozendict
from numpy.typing import NDArray
from rdkit import Chem

from .edits import AtomEditType

V = TypeVar("V")


def translate_atom_map(
    map_to: frozendict[int, int | None],
    map_from: Mapping[int, V],
    na: V | None = None,
) -> frozendict[int, V | None]:
    """
    Translate an atom map from one dictionary to another.

    :param map_to: Dictionary of atom map numbers to atom indices;
    :type map_to: frozendict[int, int | None];
    :param map_from: Dictionary of atom map numbers to atom indices;
    :type map_from: Mapping[int, V];
    :param na: Value to use for missing atom map numbers;
    :type na: V | None;
    :return: Translated atom map;
    :rtype: frozendict[int, V | None];
    """
    return frozendict(
        {
            i: map_from[j] if j is not None and j in map_from else na
            for i, j in map_to.items()
        }
    )


def extract_atom_map(mol: Chem.Mol) -> frozendict[int, int]:
    """
    Extract atom map from a RDKit molecule.

    :param mol: RDKit molecule;
    :type mol: Chem.Mol;
    :return: Atom map;
    :rtype: frozendict[int, int];
    """
    atom_map: frozendict[int, int] = frozendict()
    for atom in mol.GetAtoms():
        idx = atom.GetIdx()
        map_num = atom.GetAtomMapNum()
        atom_map = atom_map.set(idx, map_num if map_num else 0)
    return atom_map


def drop_atom_maps(mol: Chem.Mol) -> Chem.Mol:
    """
    Drop atom maps from a RDKit molecule.

    :param mol: RDKit molecule;
    :type mol: Chem.Mol;
    :return: RDKit molecule with dropped atom maps;
    :rtype: Chem.Mol;
    """
    mol = copy.deepcopy(mol)
    for atom in mol.GetAtoms():
        atom.SetAtomMapNum(0)
    return mol


def canonicalize_smiles(smiles: str) -> str:
    """Canonicalize a (possibly multi-component) SMILES string.

    Parses via ``MolFromSmarts`` so that fragment SMILES containing
    aromatic atoms outside rings (e.g. ``c:c``) are handled correctly.
    The resulting canonical form is deterministic for both single-
    and multi-component SMILES: component order and atom ordering
    are both canonicalized by RDKit.

    :param smiles: Dot-separated SMILES of one or more molecular fragments.
    :type smiles: str
    :return: Canonicalized SMILES string.
    :rtype: str
    :raises ValueError: If RDKit cannot parse the input.
    """
    mol = Chem.MolFromSmarts(smiles)
    if mol is None:
        raise ValueError(f"Failed to parse SMILES as SMARTS: {smiles!r}")
    return Chem.MolToSmiles(mol)


def detect_product_atom_change(T, p_atom_idx) -> AtomEditType:
    """
    Detect product atom has been changed.

    :param T: Reaction transform;
    :type T: ReactionTransform;
    :param p_atom_idx: Product atom index;
    :type p_atom_idx: int;
    :return: Atom edit type;
    :rtype: AtomEditType;
    """
    # atom does not appear in reactants
    if T.pR_map[p_atom_idx] is None:
        return AtomEditType.ATOM_ADDED

    p_atom = T.product.canonical_rdmol.GetAtomWithIdx(p_atom_idx)
    r_idx, r_atom_idx = T.pR_map[p_atom_idx]
    r_atom = T.reactants[r_idx].canonical_rdmol.GetAtomWithIdx(r_atom_idx)
    p_atom_neighbors = neighbor_indices(p_atom)
    r_atom_neighbors = neighbor_indices(r_atom, atom_map=T.Rp_map[r_idx])

    # fragment attached or detached
    if set(r_atom_neighbors) < set(p_atom_neighbors):
        return AtomEditType.FRAGMENT_ATTACH
    elif set(p_atom_neighbors) < set(r_atom_neighbors):
        return AtomEditType.FRAGMENT_DETACH
    elif set(r_atom_neighbors) != set(p_atom_neighbors):
        # simultaneous attach + detach (bond swap)
        return AtomEditType.FRAGMENT_ATTACH

    # properties changed
    if atoms_differ_in_properties(p_atom, r_atom):
        return AtomEditType.PROPERTY_CHANGE

    return AtomEditType.NONE


def neighbor_indices(atom, atom_map=None):
    """
    Get neighbor indices of an atom.

    :param atom: Atom;
    :type atom: Chem.Atom;
    :param atom_map: Atom map;
    :type atom_map: frozendict[int, int | None];
    :return: Neighbor indices;
    :rtype: list[int];
    """
    neighbor_indices = [n.GetIdx() for n in atom.GetNeighbors()]
    if atom_map is not None:
        # -1 represents atoms present in the reactant, but not present in the product
        neighbor_indices_remapped = []
        for idx in neighbor_indices:
            if atom_map[idx] is not None:
                if isinstance(atom_map[idx], tuple):
                    neigh_idx = atom_map[idx][1]
                else:
                    neigh_idx = atom_map[idx]
            else:
                neigh_idx = -1
            neighbor_indices_remapped.append(neigh_idx)
        neighbor_indices = neighbor_indices_remapped
    return sorted(neighbor_indices)


def atoms_differ_in_properties(atom_1, atom_2):
    """
    Check if two atoms differ in properties.

    :param atom_1: First atom;
    :type atom_1: Chem.Atom;
    :param atom_2: Second atom;
    :type atom_2: Chem.Atom;
    :return: True if atoms differ in properties, False otherwise;
    :rtype: bool;
    """
    if atom_1.GetAtomicNum() != atom_2.GetAtomicNum():
        return True
    elif atom_1.GetNumRadicalElectrons() != atom_2.GetNumRadicalElectrons():
        return True
    elif atom_1.GetFormalCharge() != atom_2.GetFormalCharge():
        return True
    elif atom_1.GetTotalNumHs() != atom_2.GetTotalNumHs():
        return True
    return False


def return_index_for_atom_map(m, atom_map):
    """
    Return atom index for atom with a given atom map.

    :param m: Molecule;
    :type m: Chem.Mol;
    :param atom_map: Atom map;
    :type atom_map: int;
    :return: Index;
    :rtype: int | None;
    """
    for a in m.GetAtoms():
        if a.GetAtomMapNum() == atom_map:
            return a.GetIdx()
    return None


def smarts_to_pattern_fingerprint(pattern: Chem.Mol, fp_length: int) -> NDArray:
    """
    Generates a pattern fingerprint for a SMARTS in the form of Chem.Mol.

    :param pattern: pattern;
    :type pattern: Chem.Mol;
    :param fp_length: fingerprint length;
    :type fp_length: int;
    :return: Pattern fingerprint;
    :rtype: NDArray;
    """
    fp = Chem.PatternFingerprint(pattern, fp_length)
    arr = np.zeros(fp_length, dtype=np.uint8)
    arr[np.array(fp.GetOnBits())] = 1
    return arr
