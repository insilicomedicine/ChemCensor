from rdkit import Chem

from chemcensor.extraction.utils import find_symmetric_matches
from chemcensor.extraction.utils import MAX_AUTOMORPHISMS_FOR_SYMMETRIC_EXPANSION


# Reactant of the reaction that used to hang scoring: a polyol masked by four
# bulky silyl protecting groups. Its automorphism group is huge (>100k), which
# made the VF2 subgraph search in ``find_symmetric_matches`` explode and hang.
PATHOLOGICAL_SILYL_SMILES = (
    "C=CC[C@H](C[C@H](C[C@H](C[C@H](C)O[Si](C(C)C)(C(C)C)C(C)C)"
    "O[Si]([Si](C)(C)C)([Si](C)(C)C)[Si](C)(C)C)O[Si]([Si](C)(C)C)"
    "([Si](C)(C)C)[Si](C)(C)C)O[Si]([Si](C)(C)C)([Si](C)(C)C)[Si](C)(C)C"
)


def test_returns_empty_when_pattern_covers_whole_molecule() -> None:
    mol = Chem.MolFromSmiles("CCO")
    pattern = Chem.MolFromSmarts("CCO")

    assert find_symmetric_matches(mol, pattern) == ()


def test_skips_pathologically_symmetric_molecule() -> None:
    """Regression: must return quickly instead of hanging in VF2 matching.

    Without the automorphism guard, matching the large fragment below against
    this highly symmetric molecule never returns.
    """
    mol = Chem.MolFromSmiles(PATHOLOGICAL_SILYL_SMILES)

    # A large fragment of the molecule (drop a couple of atoms so the
    # whole-molecule early-return does not trigger) — this is the kind of
    # pattern produced during reaction-center extraction.
    rw = Chem.RWMol(mol)
    rw.RemoveAtom(mol.GetNumAtoms() - 1)
    rw.RemoveAtom(mol.GetNumAtoms() - 2)
    pattern = Chem.MolFromSmarts(Chem.MolToSmarts(rw.GetMol()))

    # Sanity: the molecule really is pathologically symmetric.
    self_matches = mol.GetSubstructMatches(
        mol, uniquify=False, maxMatches=MAX_AUTOMORPHISMS_FOR_SYMMETRIC_EXPANSION
    )
    assert len(self_matches) >= MAX_AUTOMORPHISMS_FOR_SYMMETRIC_EXPANSION

    assert find_symmetric_matches(mol, pattern) == ()


def test_returns_matches_for_symmetric_fragment() -> None:
    """A mildly symmetric molecule still gets its symmetric matches expanded."""
    mol = Chem.MolFromSmiles("Cc1ccc(C)cc1")  # p-xylene: two equivalent methyls
    pattern = Chem.MolFromSmarts("[CH3]")

    matches = find_symmetric_matches(mol, pattern)

    assert len(matches) == 2


def test_returns_empty_for_non_symmetric_fragment() -> None:
    """Distinct (non-equivalent) matches must not be treated as symmetric."""
    mol = Chem.MolFromSmiles("Cc1ccc(CC)cc1")  # methyl vs ethyl: not equivalent
    pattern = Chem.MolFromSmarts("[CH3]")

    assert find_symmetric_matches(mol, pattern) == ()
