import pytest

from chemcensor.basic import Reaction
from chemcensor.basic import ReactionTransform
from chemcensor.basic import SENTINEL
from chemcensor.processing.errors.sis_annotator_errors import (
    SisAnnotatorEmptyTransformError,
)
from chemcensor.processing.errors.sis_annotator_errors import (
    SisAnnotatorInconsistentStaticCentersError,
)
from chemcensor.processing.errors.static_stereo_validator_errors import (
    StaticStereoValidatorInconsistentStaticAtomStereoError,
)
from chemcensor.processing.errors.static_stereo_validator_errors import (
    StaticStereoValidatorInconsistentStaticBondStereoError,
)
from chemcensor.processing.reaction_processor import ReactionProcessor
from chemcensor.processing.sis_annotator import SisAnnotator

SIS_REACTIONS_WITH_MULTIPLE_CENTERS = (
    "COc1noc(c2c(N(CC3CCC(CC3)c4ncccc4)C)c[nH]n2)c1>>COc5noc(c6c(N(C[C@H]7CC[C@H]"
    "(CC7)c8ncccc8)C)c[nH]n6)c5",
    "CC1CC(C1)O>>C[C@H]2C[C@@H](C2)O",
    "CC1CC(C1)Br>>C[C@H]2C[C@H](C2)Br",
    "COc1cnc(n(nc2)c3c2c(C4CC4)cc(OC5CC(C5)C)n3)cc1>>COc6cnc(n(nc7)c8c7c(C9CC9)"
    "cc(O[C@@H]%10C[C@@H](C%10)C)n8)cc6",
    "CC(F)CC(C1CCCC1)C(N)=O>>C[C@@H](F)C[C@H](C2CCCC2)C(N)=O",
)

FALSE_SIS_REACTIONS_WITH_MULTIPLE_CENTERS = (
    "CC(=O)[O-].O=[N+]([O-])c1ccc(OC2O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]2O)cc1."
    "OC1CN2CCCC(O)C2C1O.[Na+]>>"
    "O[C@H]1[C@H]2[C@H](O)CCCN2C[C@H]1O",
    "CC=CC=CC>>C/C=C/C=C/C",
)


@pytest.fixture
def sis_reaction() -> Reaction:
    return Reaction(
        reaction_smiles="",
        reaction_transform=ReactionTransform.from_reaction_smiles(
            "[CH3:1][C:2](=[O:3])[CH:4]1[CH2:5][C@@H:6]2[CH2:7]"
            "[CH2:8][CH2:9][C@H:10]1[CH2:11][CH2:12]2>>[CH3:1]"
            "[C:2](=[O:3])[C@H:4]1[CH2:5][C@@H:6]2[CH2:7][CH2:8]"
            "[CH2:9][C@H:10]1[CH2:11][CH2:12]2"
        ),
    )


@pytest.fixture
def empty_transform_reaction() -> Reaction:
    return Reaction(
        reaction_smiles="",
    )


@pytest.fixture
def not_sis_reaction() -> Reaction:
    return Reaction(
        reaction_smiles="",
        reaction_transform=ReactionTransform.from_reaction_smiles(
            "[CH3:1][C:2]([CH3:3])([OH:4])[c:5]1[cH:6][c:7]([C:8]([F:9])"
            "([F:10])[F:11])[n:12][cH:13][c:14]1-[c:15]1[cH:16][cH:17]"
            "[c:18]([C:19]2([C:20]#N)[CH2:23][O:24][CH2:25]2)[cH:26]"
            "[cH:27]1.[OH-:21].[OH2:22]>>[CH3:1][C:2]([CH3:3])([OH:4])"
            "[c:5]1[cH:6][c:7]([C:8]([F:9])([F:10])[F:11])[n:12][cH:13]"
            "[c:14]1-[c:15]1[cH:16][cH:17][c:18]([C:19]2([C:20](=[O:21])"
            "[OH:22])[CH2:23][O:24][CH2:25]2)[cH:26][cH:27]1"
        ),
    )


@pytest.fixture
def batch(sis_reaction, empty_transform_reaction, not_sis_reaction):
    return [
        sis_reaction,
        empty_transform_reaction,
        not_sis_reaction,
    ]


def test_sis_annotator_empty_transform(empty_transform_reaction: Reaction):
    sis_annotator = SisAnnotator()
    with pytest.raises(SisAnnotatorEmptyTransformError):
        sis_annotator.process(empty_transform_reaction)


def test_sis_annotator_true(sis_reaction: Reaction):
    sis_annotator = SisAnnotator()
    sis_reaction = sis_annotator.process(sis_reaction)
    assert sis_reaction.is_sis_reaction is True


def test_sis_annotator_false_not_sis(not_sis_reaction: Reaction):
    sis_annotator = SisAnnotator()
    not_sis_reaction = sis_annotator.process(not_sis_reaction)
    assert not_sis_reaction.is_sis_reaction is False


@pytest.mark.parametrize(
    "reaction_smiles",
    list(SIS_REACTIONS_WITH_MULTIPLE_CENTERS),
    ids=[i for i in range(len(SIS_REACTIONS_WITH_MULTIPLE_CENTERS))],
)
def test_multi_center_sis_examples_target_classified_as_sis(
    reaction_smiles: str,
) -> None:
    """``?`` → ``R/S`` or pseudo ``r``/``s`` on product; full pipeline marks SIS."""
    processed = ReactionProcessor().process(Reaction(reaction_smiles=reaction_smiles))
    assert processed.is_sis_reaction is True


_STATIC_STEREO_MISMATCH = (
    StaticStereoValidatorInconsistentStaticAtomStereoError,
    StaticStereoValidatorInconsistentStaticBondStereoError,
)


@pytest.mark.parametrize(
    "reaction_smiles",
    list(FALSE_SIS_REACTIONS_WITH_MULTIPLE_CENTERS),
    ids=("multifrag_over_sis_atom_cap", "diene_over_sis_alkene_cap"),
)
def test_multi_center_false_sis_examples_fail_static_stereo_validation(
    reaction_smiles: str,
) -> None:
    """Too many simultaneous resolutions for :class:`SisConfig` caps → not SIS.

    Then :class:`~chemcensor.processing.static_stereo_validator.StaticStereoValidator`
    runs and rejects the apparent static-stereo mismatch (atom or bond), so the
    full pipeline raises instead of returning ``is_sis_reaction is False``.
    """
    with pytest.raises(_STATIC_STEREO_MISMATCH):
        ReactionProcessor().process(Reaction(reaction_smiles=reaction_smiles))


def test_alkene_stereoresolution_multi_reactant_is_sis():
    """E/Z stereoresolution on alkene (SIS): unassigned → assigned; solvents unmapped.

    Mapper + OrphanRemover leave a single mapped reactant; SisAnnotator marks SIS.
    """
    reaction_smiles = (
        r"CC(=Cc1ccc(C(=O)O)cc1)c1ccc(O)c(C(C)(C)C)c1.CCCCCC.CCOCC.CN(C)C=O.C[S-]"
        r".[Li+]>>C/C(=C\c1ccc(C(=O)O)cc1)c1ccc(O)c(C(C)(C)C)c1"
    )
    reaction = Reaction(reaction_smiles=reaction_smiles)
    processed = ReactionProcessor().process(reaction)
    assert processed.is_sis_reaction is True


def test_atom_stereoresolution_with_cip_descriptor_shift_is_sis():
    reaction_smiles = (
        "NC(Cc1ccnc(Oc2ccccc2-c2ccccc2-c2ccc(=O)n([C@@H]3C[C@H](F)C3)c2)c1)C(=O)O"
        ">>N[C@@H](Cc1ccnc(Oc2ccccc2-c2ccccc2-c2ccc(=O)n([C@@H]3C[C@H](F)C3)c2)"
        "c1)C(=O)O"
    )
    reaction = Reaction(reaction_smiles=reaction_smiles)

    processed = ReactionProcessor().process(reaction)

    assert processed.is_sis_reaction is True


def test_atom_stereoresolution_with_pseudo_to_asymmetric_shift_is_sis():
    reaction_smiles = (
        "NC(Cc1ccnc(Oc2ccccc2-c2ccccc2-c2ccc(=O)n([C@@H]3C[C@H](F)C3)c2)c1)C(=O)O"
        ">>N[C@@H](Cc1ccnc(Oc2ccccc2-c2ccccc2-c2ccc(=O)n([C@@H]3C[C@H](F)C3)c2)"
        "c1)C(=O)O"
    )
    reaction = Reaction(reaction_smiles=reaction_smiles)

    processed = ReactionProcessor().process(reaction)

    assert processed.is_sis_reaction is True


def test_pure_static_stereo_inversion_raises_sis_error():
    reaction_smiles = (
        "[CH3:1][C:2]([C@@H:4]1[CH2:5][C@@H:6]2[CH2:7][CH2:8]"
        "[CH2:9][C@H:10]1[CH2:11][CH2:12]2)=[O:3]>>[CH3:1][C:2]"
        "([C@H:4]3[CH2:5][C@@H:6]4[CH2:7][CH2:8][CH2:9][C@H:10]3"
        "[CH2:11][CH2:12]4)=[O:3]"
    )
    reaction = Reaction(reaction_smiles=reaction_smiles)

    with pytest.raises(SisAnnotatorInconsistentStaticCentersError):
        ReactionProcessor().process(reaction)


def test_pure_static_alkene_stereo_loss_raises_sis_error():
    reaction_smiles = r"[CH3:1]/[CH:2]=[CH:3]/[CH3:4]>>[CH3:1][CH:2]=[CH:3][CH3:4]"
    reaction = Reaction(reaction_smiles=reaction_smiles)

    with pytest.raises(SisAnnotatorInconsistentStaticCentersError):
        ReactionProcessor().process(reaction)


def test_pure_static_alkene_stereo_inversion_raises_sis_error():
    reaction_smiles = (
        r"CC#N.Cc1oc(-c2ccccc2)nc1CCOc1ccc(/C=C2\SC(=O)NC2=O)cc1>>"
        r"Cc1oc(-c2ccccc2)nc1CCOc1ccc(/C=C2/SC(=O)NC2=O)cc1"
    )
    reaction = Reaction(reaction_smiles=reaction_smiles)

    with pytest.raises(SisAnnotatorInconsistentStaticCentersError):
        ReactionProcessor().process(reaction)


def test_process_batch(batch):
    """process_batch() passes sentinels through and marks failures as dummy."""
    sis_annotator = SisAnnotator()
    results = sis_annotator.process_batch(batch)
    assert len(results) == len(batch)
    assert not results[0].dummy
    assert results[0].is_sis_reaction is True
    assert results[1].dummy
    assert results[1] is SENTINEL
    assert not results[2].dummy
