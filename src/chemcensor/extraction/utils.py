import copy

from rdkit import Chem

# Upper bound on the molecule's automorphism count above which symmetric-match
# expansion is skipped. Highly symmetric molecules (e.g. multiple equivalent
# silyl protecting groups) make the VF2 subgraph search in
# ``GetSubstructMatches`` below blow up combinatorially and effectively hang.
# The value 1000 was selected as a number of automorphisms for a reactant
# from tests (see test_utils.py)
MAX_AUTOMORPHISMS_FOR_SYMMETRIC_EXPANSION = 1000


def clean_hydrogens_from_smarts(smarts: str, keep_stars: bool = True) -> str:
    """Remove hydrogens from SMARTS string.

    :param smarts: SMARTS string to process
    :type smarts: str
    :param keep_stars: Whether to keep chiral markers (@)
    :type keep_stars: bool

    :return: SMARTS string with hydrogens removed
    :rtype: str
    """
    if not keep_stars:
        smarts = smarts.replace("@", "")

    # Replace hydrogen patterns in order of specificity
    replacements = [
        ("H4+:", ":"),
        ("H3+:", ":"),
        ("H2+:", ":"),
        ("H+:", ":"),
        ("H3:", ":"),
        ("H2:", ":"),
        ("H1:", ":"),
        ("H:", ":"),
        ("H-:", ":"),
    ]

    for old, new in replacements:
        smarts = smarts.replace(old, new)

    return smarts


def find_symmetric_matches(
    mol: Chem.Mol, pattern: Chem.Mol
) -> tuple[tuple[int, ...], ...]:
    """Return substructure matches that require index expansion.

    If the molecule has multiple equivalent (symmetric) matches for
    *pattern*, those matches are returned.
    Otherwise, an empty tuple is returned.

    :param mol: Molecule to search.
    :type mol: Chem.Mol
    :param pattern: Query fragment.
    :type pattern: Chem.Mol
    :return: Matches requiring expansion, or ``()`` if none.
    :rtype: tuple[tuple[int, ...], ...]
    """
    # Fragment covers the whole molecule → nothing to expand
    if pattern.GetNumAtoms() == mol.GetNumAtoms():
        return ()

    # Guard against pathologically symmetric molecules
    self_matches = mol.GetSubstructMatches(
        mol,
        uniquify=False,
        maxMatches=MAX_AUTOMORPHISMS_FOR_SYMMETRIC_EXPANSION,
    )
    if len(self_matches) >= MAX_AUTOMORPHISMS_FOR_SYMMETRIC_EXPANSION:
        return ()

    mol = copy.deepcopy(mol)
    for atom in mol.GetAtoms():
        atom.SetAtomMapNum(0)

    matches = mol.GetSubstructMatches(pattern, maxMatches=5)

    # Single match or too many matches → nothing to expand
    if len(matches) <= 1 or len(matches) >= 5:
        return ()

    # Check whether all matches are symmetrically equivalent
    match_intersection = set.intersection(*(set(m) for m in matches))
    smiles_set: set[str] = set()
    for match in matches:
        mol_copy = copy.deepcopy(mol)
        for i, atom_idx in enumerate(match):
            if atom_idx not in match_intersection:
                atom = mol_copy.GetAtomWithIdx(atom_idx)
                atom.SetIsotope(100)
        smiles_set.add(Chem.MolToSmiles(mol_copy))

    if len(smiles_set) == 1:
        return matches

    return ()


def is_ring_atoms_within_indices(mol: Chem.Mol, atom_indices: list[int]) -> bool:
    """
    Check if any of the given atom indices are part of a ring.

    :param mol: RDKit Mol object
    :type mol: Chem.Mol
    :param atom_indices: List of atom indices to check
    :type atom_indices: list[int]

    :return: True if any atom is in a ring, False otherwise
    :rtype: bool
    """
    ring_info = mol.GetRingInfo()
    for ring in ring_info.AtomRings():
        if set(ring) & set(atom_indices):
            return True
    return False
