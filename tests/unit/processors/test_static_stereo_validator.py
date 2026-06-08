import pytest

from chemcensor.basic import Reaction
from chemcensor.basic import ReactionTransform
from chemcensor.basic import SENTINEL
from chemcensor.processing.errors.static_stereo_validator_errors import (
    StaticStereoValidatorEmptyTransformError,
)
from chemcensor.processing.errors.static_stereo_validator_errors import (
    StaticStereoValidatorInconsistentStaticAtomStereoError,
)
from chemcensor.processing.errors.static_stereo_validator_errors import (
    StaticStereoValidatorInconsistentStaticBondStereoError,
)
from chemcensor.processing.reaction_processor import ReactionProcessor
from chemcensor.processing.static_stereo_validator import StaticStereoValidator


@pytest.fixture
def empty_transform_reaction() -> Reaction:
    return Reaction(reaction_smiles="")


@pytest.fixture
def inconsistent_static_center_reaction() -> Reaction:
    reaction_smiles = (
        "[OH:1][C:2]([C@H:4]1[CH2:5][C@@H:6]2[CH2:7][CH2:8][CH2:9][C@H:10]1"
        "[CH2:11][CH2:12]2)=[O:3]>>[O:3]=[C:2]([C@H:4]3[CH2:5][C@H:6]4"
        "[CH2:7][CH2:8][CH2:9][C@H:10]3[CH2:11][CH2:12]4)[O:1]C"
    )
    return Reaction(
        reaction_smiles=reaction_smiles,
        reaction_transform=ReactionTransform.from_reaction_smiles(reaction_smiles),
    )


@pytest.fixture
def consistent_static_reaction() -> Reaction:
    reaction_smiles = (
        "[OH:1][C:2]([C@H:4]1[CH2:5][C@@H:6]2[CH2:7][CH2:8][CH2:9][C@H:10]1"
        "[CH2:11][CH2:12]2)=[O:3]>>[O:3]=[C:2]([C@H:4]3[CH2:5][C@@H:6]4"
        "[CH2:7][CH2:8][CH2:9][C@H:10]3[CH2:11][CH2:12]4)[O:1]C"
    )
    return Reaction(
        reaction_smiles=reaction_smiles,
        reaction_transform=ReactionTransform.from_reaction_smiles(reaction_smiles),
    )


@pytest.fixture
def consistent_static_sulfur_reaction() -> Reaction:
    reaction_smiles = (
        "[CH3:1][S@](=[O:9])([CH2:3][Br:5])[CH:6]([CH3:7])[CH3:8]>>"
        "[CH3:1][S@](=[O:9])([CH2:3][OH:5])[CH:6]([CH3:7])[CH3:8]"
    )
    return Reaction(
        reaction_smiles=reaction_smiles,
        reaction_transform=ReactionTransform.from_reaction_smiles(reaction_smiles),
    )


@pytest.fixture
def inconsistent_static_sulfur_reaction() -> Reaction:
    reaction_smiles = (
        "[CH3:1][S@](=[O:9])([CH2:3][Br:5])[CH:6]([CH3:7])[CH3:8]>>"
        "[CH3:1][S@@](=[O:9])([CH2:3][OH:5])[CH:6]([CH3:7])[CH3:8]"
    )
    return Reaction(
        reaction_smiles=reaction_smiles,
        reaction_transform=ReactionTransform.from_reaction_smiles(reaction_smiles),
    )


@pytest.fixture
def validator_batch(
    consistent_static_reaction: Reaction,
    empty_transform_reaction: Reaction,
    inconsistent_static_center_reaction: Reaction,
    lost_stereo_center_reaction: Reaction,
):
    return [
        consistent_static_reaction,
        empty_transform_reaction,
        inconsistent_static_center_reaction,
        lost_stereo_center_reaction,
    ]


def test_static_stereo_validator_empty_transform(
    empty_transform_reaction: Reaction,
):
    validator = StaticStereoValidator()
    with pytest.raises(StaticStereoValidatorEmptyTransformError):
        validator.process(empty_transform_reaction)


def test_static_stereo_validator_passes_consistent_reaction(
    consistent_static_reaction: Reaction,
):
    validator = StaticStereoValidator()
    validated = validator.process(consistent_static_reaction)
    assert validated is consistent_static_reaction


def test_static_stereo_validator_raises_for_inconsistent_center(
    inconsistent_static_center_reaction: Reaction,
):
    validator = StaticStereoValidator()
    with pytest.raises(StaticStereoValidatorInconsistentStaticAtomStereoError):
        validator.process(inconsistent_static_center_reaction)


def test_static_stereo_validator_passes_consistent_sulfur_center(
    consistent_static_sulfur_reaction: Reaction,
):
    validator = StaticStereoValidator()
    validated = validator.process(consistent_static_sulfur_reaction)
    assert validated is consistent_static_sulfur_reaction


def test_static_stereo_validator_raises_for_inconsistent_sulfur_center(
    inconsistent_static_sulfur_reaction: Reaction,
):
    validator = StaticStereoValidator()
    with pytest.raises(StaticStereoValidatorInconsistentStaticAtomStereoError):
        validator.process(inconsistent_static_sulfur_reaction)


def test_static_stereo_validator_error_contains_reaction_smiles():
    reaction_smiles = (
        "C[O:1][C:2](=[O:3])[C@@H:4]1[CH2:5][C@@H:6]2[CH2:7]"
        "[CH2:8][CH2:9][C@H:10]1[CH2:11][CH2:12]2>>[OH:1]"
        "[C:2](=[O:3])[C@H:4]1[CH2:5][C@@H:6]2[CH2:7][CH2:8]"
        "[CH2:9][C@H:10]1[CH2:11][CH2:12]2"
    )
    reaction = Reaction(
        reaction_smiles=reaction_smiles,
        reaction_transform=ReactionTransform.from_reaction_smiles(reaction_smiles),
    )

    validator = StaticStereoValidator()
    with pytest.raises(
        StaticStereoValidatorInconsistentStaticAtomStereoError
    ) as exc_info:
        validator.process(reaction)

    assert reaction_smiles in str(exc_info.value)
    assert exc_info.value.reaction_smiles == reaction_smiles


@pytest.fixture
def lost_stereo_center_reaction() -> Reaction:
    reaction_smiles = (
        "[CH3:1][CH2:2][O:3][C:4](=[O:5])[C@@H:6]1[CH2:7][CH2:8]"
        "[CH2:9][NH:10][CH2:11]1>>[CH3:1][CH2:2][O:3][C:4](=[O:5])"
        "[CH:6]1[CH2:7][CH2:8][CH2:9][NH:10][CH2:11]1"
    )
    return Reaction(
        reaction_smiles=reaction_smiles,
        reaction_transform=ReactionTransform.from_reaction_smiles(reaction_smiles),
    )


def test_lost_stereo_center_raises_validator_error(
    lost_stereo_center_reaction: Reaction,
):
    validator = StaticStereoValidator()
    with pytest.raises(StaticStereoValidatorInconsistentStaticAtomStereoError):
        validator.process(lost_stereo_center_reaction)


def test_static_stereo_validator_process_batch(validator_batch):
    validator = StaticStereoValidator()
    results = validator.process_batch(validator_batch)
    assert len(results) == len(validator_batch)
    assert not results[0].dummy
    assert results[1].dummy
    assert results[1] is SENTINEL
    assert results[2].dummy
    assert results[2] is SENTINEL


REACTION_SMILES_WITH_CONSISTENT_STATIC_ALKENE_STEREO_NEAR_RC: tuple[str, ...] = (
    r"C/C=C/CBr>>C/C=C/CO",
    r"C/C=C/CBr>>C\C=C\CO",
    r"BrCC/C=C/C>>OCC/C=C/C",
    r"BrCC/C=C/C>>OCC\C=C\C",
    r"C/C=C(CC)/CC(N)=O>>C/C=C(C(C)=O)/CC(N)=O",
    r"C/C=C(CC)/CC(N)=O>>C\C=C(C(C)=O)\CC(N)=O",
)


@pytest.mark.parametrize(
    "reaction_smiles",
    REACTION_SMILES_WITH_CONSISTENT_STATIC_ALKENE_STEREO_NEAR_RC,
)
def test_consistent_static_alkene_stereo_near_the_rc(
    reaction_smiles: str,
):
    reaction = Reaction(reaction_smiles=reaction_smiles)
    processed = ReactionProcessor().process(reaction)
    assert processed.dummy is False
    assert processed.is_sis_reaction is False


REACTION_SMILES_WITH_INCONSISTENT_STATIC_ALKENE_STEREO_NEAR_RC: tuple[str, ...] = (
    r"C/C=C/CBr>>C/C=C\CO",
    r"BrCC/C=C/C>>OCC/C=C\C",
    r"CC/C(CC(N)=O)=C/Br>>Br/C=C(CC(N)=O)\C(C)=O",
)


@pytest.mark.parametrize(
    "reaction_smiles",
    REACTION_SMILES_WITH_INCONSISTENT_STATIC_ALKENE_STEREO_NEAR_RC,
)
def test_inconsistent_static_alkene_stereo_near_the_rc_raises(
    reaction_smiles: str,
):
    reaction = Reaction(reaction_smiles=reaction_smiles)
    with pytest.raises(StaticStereoValidatorInconsistentStaticBondStereoError):
        ReactionProcessor().process(reaction)


REACTION_SMILES_WITH_INCONSISTENT_STATIC_CENTERS: tuple[str, ...] = (
    "C=Cc1nc2ccccc2n1-c1nnc(C2CC2)[nH]1.CN[C@@H](C)C(=O)O>>"
    "C[C@H](C(=O)O)N(C)CCc1nc2ccccc2n1-c1nnc(C2CC2)[nH]1",
    "C=Cc1nc2ccccc2n1-c1nnc(C2CC2)[nH]1.CN[C@@H](C)C(=O)O>>"
    "C[C@H](C(=O)O)N(C)CCc1nc2ccccc2n1-c1nnc(C2CC2)[nH]1",
    "CN.CNCC1(CCCC1)c2ccc([C@@H]3CO3)cc2>>CNC[C@H](c4ccc(C5(CCCC5)CNC)cc4)O",
    "C[C@@H]1CCCN1.Cc(cc2)cc3n2ncc3c4oc(N5CCC(CC5)=O)nc4>>"
    "Cc(cc6)cc7n6ncc7c8oc(N9CCC(CC9)N%10CCC[C@@H]%10C)nc8",
    "CCN(S(C)(=O)=O)c1cc(C(Nc(ncc2c3ccccc3)[nH]c2=O)C)ccc1>>"
    "CCN(S(C)(=O)=O)c4cc([C@H](Nc5nc(O)c(c6ccccc6)cn5)C)ccc4",
)


@pytest.mark.parametrize(
    "reaction_smiles",
    REACTION_SMILES_WITH_INCONSISTENT_STATIC_CENTERS,
)
def test_inconsistent_static_centers_near_the_rc_raise(
    reaction_smiles: str,
):
    reaction = Reaction(reaction_smiles=reaction_smiles)
    with pytest.raises(StaticStereoValidatorInconsistentStaticAtomStereoError):
        ReactionProcessor().process(reaction)


REACTION_SMILES_WITH_CONSISTENT_STATIC_CENTERS: tuple[str, ...] = (
    "C[C@H](COC)CBr>>C[C@H](COC)CO",
    "C[C@H](CCOC)CCBr>>C[C@H](CCOC)CCO",
)


@pytest.mark.parametrize(
    "reaction_smiles",
    REACTION_SMILES_WITH_CONSISTENT_STATIC_CENTERS,
)
def test_consistent_static_centers_near_the_rc_pass(
    reaction_smiles: str,
):
    reaction = Reaction(reaction_smiles=reaction_smiles)
    processed = ReactionProcessor().process(reaction)
    assert processed.dummy is False
    assert processed.is_sis_reaction is False


# Reactions where a remote change (re)symmetrizes the molecule, so an assigned
# R/S reactant center legitimately becomes a pseudoasymmetric r/s product
# center. This is a CIP relabeling, not a static stereo mismatch.
REACTION_SMILES_WITH_RS_TO_PSEUDOASYMMETRIC_STATIC_CENTERS: tuple[str, ...] = (
    # TMS deprotection: the base-bearing ring carbon turns R -> r once both
    # ring arms become identical -CH2-CH(OH)-.
    "C[Si](C)(C)O[C@@H]1C[C@H](n2cnc3c(N)nc(N)nc32)C[C@@H]1O>>"
    "Nc1nc(N)c2ncn([C@H]3C[C@@H](O)[C@@H](O)C3)c2n1",
)


@pytest.mark.parametrize(
    "reaction_smiles",
    REACTION_SMILES_WITH_RS_TO_PSEUDOASYMMETRIC_STATIC_CENTERS,
)
def test_rs_to_pseudoasymmetric_static_center_passes(
    reaction_smiles: str,
):
    reaction = Reaction(reaction_smiles=reaction_smiles)
    processed = ReactionProcessor().process(reaction)
    assert processed.dummy is False
    assert processed.is_sis_reaction is False
