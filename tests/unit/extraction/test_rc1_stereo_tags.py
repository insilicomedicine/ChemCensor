import random

import pytest
from rdkit import Chem

from chemcensor.basic import Reaction
from chemcensor.basic.reaction_center import ReactionCenterType
from chemcensor.basic.reaction_transform import ReactionTransform
from chemcensor.extraction.extractor import Extractor

INVERSION_ETHYL = (
    "O[C@H:3]([CH2:2][CH3:1])[c:4]1[cH:5][cH:6][cH:7][cH:8][cH:9]1."
    "[nH:10]1[cH:11][cH:12][cH:13][n:14]1>>"
    "[CH3:1][CH2:2][C@H:3]([c:4]1[cH:5][cH:6][cH:7][cH:8][cH:9]1)"
    "[n:10]1[cH:11][cH:12][cH:13][n:14]1"
)
ENANTIOMER = (
    "O[C@@H:3]([CH2:2][CH3:1])[c:4]1[cH:5][cH:6][cH:7][cH:8][cH:9]1."
    "[nH:10]1[cH:11][cH:12][cH:13][n:14]1>>"
    "[CH3:1][CH2:2][C@@H:3]([c:4]1[cH:5][cH:6][cH:7][cH:8][cH:9]1)"
    "[n:10]1[cH:11][cH:12][cH:13][n:14]1"
)
RETENTION = (
    "O[C@H:3]([CH2:2][CH3:1])[c:4]1[cH:5][cH:6][cH:7][cH:8][cH:9]1."
    "[nH:10]1[cH:11][cH:12][cH:13][n:14]1>>"
    "[CH3:1][CH2:2][C@@H:3]([c:4]1[cH:5][cH:6][cH:7][cH:8][cH:9]1)"
    "[n:10]1[cH:11][cH:12][cH:13][n:14]1"
)
ANALOGUE_PROPYL = (
    "O[C@H:4]([CH2:3][CH2:2][CH3:1])[c:5]1[cH:6][cH:7][cH:8][cH:9][cH:10]1."
    "[nH:11]1[cH:12][cH:13][cH:14][n:15]1>>"
    "[CH3:1][CH2:2][CH2:3][C@H:4]([c:5]1[cH:6][cH:7][cH:8][cH:9][cH:10]1)"
    "[n:11]1[cH:12][cH:13][cH:14][n:15]1"
)
ANALOGUE_BUTYL = (
    "O[C@H:5]([CH2:4][CH2:3][CH2:2][CH3:1])[c:6]1[cH:7][cH:8][cH:9][cH:10][cH:11]1."
    "[nH:12]1[cH:13][cH:14][cH:15][n:16]1>>"
    "[CH3:1][CH2:2][CH2:3][CH2:4][C@H:5]([c:6]1[cH:7][cH:8][cH:9][cH:10][cH:11]1)"
    "[n:12]1[cH:13][cH:14][cH:15][n:16]1"
)
NO_STEREO = (
    "O[CH:3]([CH2:2][CH3:1])[c:4]1[cH:5][cH:6][cH:7][cH:8][cH:9]1."
    "[nH:10]1[cH:11][cH:12][cH:13][n:14]1>>"
    "[CH3:1][CH2:2][CH:3]([c:4]1[cH:5][cH:6][cH:7][cH:8][cH:9]1)"
    "[n:10]1[cH:11][cH:12][cH:13][n:14]1"
)


def rc1_smiles(mapped_reaction_smiles: str) -> str:
    """Extract the RC1 reaction center SMILES for an atom-mapped reaction.

    :param mapped_reaction_smiles: Atom-mapped reaction SMILES.
    :type mapped_reaction_smiles: str
    :return: ``reaction_center_smiles`` of the RC1 center.
    :rtype: str
    """
    reaction = Reaction(
        reaction_smiles=mapped_reaction_smiles,
        reaction_transform=ReactionTransform.from_reaction_smiles(
            mapped_reaction_smiles
        ),
    )
    extracted = Extractor(max_center_type=ReactionCenterType.RC1).extract_rc(reaction)
    return extracted.get_reaction_center_by_type(
        ReactionCenterType.RC1
    ).reaction_center_smiles


@pytest.mark.parametrize(
    "mapped_reaction_smiles",
    [INVERSION_ETHYL, ENANTIOMER, RETENTION],
    ids=["inversion", "enantiomer", "retention"],
)
def test_rc1_keeps_stereo_tag(mapped_reaction_smiles: str) -> None:
    """RC1 records the tag even though the substituents are truncated."""
    assert "@" in rc1_smiles(mapped_reaction_smiles)


def test_rc1_separates_enantiomers() -> None:
    """Mirror-image substrates must not collapse onto the same RC1 key."""
    assert rc1_smiles(INVERSION_ETHYL) != rc1_smiles(ENANTIOMER)


def test_rc1_separates_retention_from_inversion() -> None:
    """Retention and inversion at the reacting centre are different centers."""
    assert rc1_smiles(INVERSION_ETHYL) != rc1_smiles(RETENTION)


@pytest.mark.parametrize(
    "analogue",
    [ANALOGUE_PROPYL, ANALOGUE_BUTYL],
    ids=["propyl", "butyl"],
)
def test_rc1_ignores_distant_differences(analogue: str) -> None:
    """Lengthening the alkyl arm is invisible at RC1, so the key must not change.

    Without this, every chain length would get its own key and reference-database
    hits would scatter across near-duplicate centers.
    """
    assert rc1_smiles(analogue) == rc1_smiles(INVERSION_ETHYL)


def test_rc1_stays_tag_free_without_stereo() -> None:
    """A substrate with no defined configuration keeps its plain RC1 key."""
    assert "@" not in rc1_smiles(NO_STEREO)


def renumber_atoms(mapped_reaction_smiles: str, seed: int) -> str:
    """Rewrite a reaction SMILES with the atoms of each component shuffled.

    The molecules, their atom maps and their stereochemistry are unchanged —
    only the order in which the atoms are written down differs.

    :param mapped_reaction_smiles: Atom-mapped reaction SMILES.
    :type mapped_reaction_smiles: str
    :param seed: Seed for the shuffle, so the case names a reproducible order.
    :type seed: int
    :return: The same reaction with permuted atom order.
    :rtype: str
    """
    rng = random.Random(seed)
    sides: list[str] = []
    for side in mapped_reaction_smiles.split(">>"):
        components: list[str] = []
        for component in side.split("."):
            mol = Chem.MolFromSmiles(component)
            order = list(range(mol.GetNumAtoms()))
            rng.shuffle(order)
            components.append(
                Chem.MolToSmiles(Chem.RenumberAtoms(mol, order), canonical=False)
            )
        sides.append(".".join(components))
    return ">>".join(sides)


@pytest.mark.parametrize("seed", range(5))
def test_rc1_is_stable_under_atom_renumbering(seed: int) -> None:
    """The key is a database lookup key, so input atom order must not reach it.

    The tag is written from the fragment's canonical atom ranking, and at RC1
    the substituents it ranks are truncated stubs — if that ranking depended on
    how the input happened to be numbered, the same reaction would land under
    two different keys.
    """
    shuffled = renumber_atoms(INVERSION_ETHYL, seed)
    assert shuffled != INVERSION_ETHYL
    assert rc1_smiles(shuffled) == rc1_smiles(INVERSION_ETHYL)
