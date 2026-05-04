from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from chemcensor.basic import Reaction
from chemcensor.basic import ReactionCenterType
from chemcensor.basic import SENTINEL
from chemcensor.basic.reaction_transform import ReactionTransform
from chemcensor.extraction.errors import MissingReactingAtomsError
from chemcensor.extraction.errors import MissingReactionTransformError
from chemcensor.extraction.errors import ReactionCenterExtractorError
from chemcensor.extraction.reaction_center_extractor import ReactionCenterExtractor
from chemcensor.processing.reaction_processor import DEFAULT_PROCESSORS
from chemcensor.processing.reaction_processor import ReactionProcessor
from chemcensor.rules.functional_groups import FG_SIGNATURE_LENGTH

REACTION_CENTERS_FIXTURES_PATH = (
    Path(__file__).resolve().parent / "fixtures" / "reaction_centers_fixtures.json"
)

REACTIONS_LIST: list[str] = [
    "CCN(S(C)(=O)=O)c1cc([C@H](Nc(ncc2c3ccccc3)[nH]c2=O)C)ccc1>>"
    "CCN(S(C)(=O)=O)c4cc([C@H](Nc5nc(O)c(c6ccccc6)cn5)C)ccc4",
    "CC1=CC=NN1>>CC2=NNC=C2",
    "Nc1nc(O)c(c2ccccc2)cn1>>Nc(ncc1c2ccccc2)[nH]c1=O",
    "CC1=CC=CC2=NNC=C12>>CC3=CC=CC4=C3C=NN4",
    "OC1=CC=CC=N1>>O=C2C=CC=CN2",
    "O=C1C=C(C)N=CN1>>O=C2C=C(C)NC=N2",
    "O=C1C=C(C)NC=N1>>O=C2C=C(C)N=CN2",
    "OC1=NC=CC=N1>>O=C2N=CC=CN2",
    "OC1=CC=NC=C1>>O=C2C=CNC=C2",
    "O=C1C=CNC=C1>>OC2=CC=NC=C2",
    "CC1=CN=CN1>>CC2=CNC=N2",
    "CC1=CNC=N1>>CC2=CN=CN2",
    "CC1=CNN=N1>>CC2=NNN=C2",
    "CC1=NNN=C1>>CC2=CNN=N2",
    "CC1=NN=CN1>>CC2=NC=NN2",
    "Cc1nnc[nH]1>>Cc2nc[nH]n2",
]


@pytest.fixture
def reactions_list() -> list[str]:
    """Unmapped tautomerization reaction SMILES."""
    return list(REACTIONS_LIST)


@pytest.fixture
def processor() -> ReactionProcessor:
    return ReactionProcessor(processors=DEFAULT_PROCESSORS)


@pytest.fixture
def rc_extractor() -> ReactionCenterExtractor:
    return ReactionCenterExtractor(max_center_type=ReactionCenterType.RC4)


@pytest.fixture
def zero_fg_signature() -> np.ndarray:
    return np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)


@pytest.mark.parametrize(
    "reaction_smiles",
    REACTIONS_LIST,
    ids=lambda s: s[:40] + ".." if len(s) > 40 else s,
)
def test_tautomerization_reactions_are_detected(
    reaction_smiles: str,
    processor: ReactionProcessor,
    rc_extractor: ReactionCenterExtractor,
    zero_fg_signature: np.ndarray,
) -> None:
    """Each reaction in the list is a tautomerization;
    extractor should set is_tautomerization_reaction."""
    reaction = Reaction(reaction_smiles=reaction_smiles)
    reaction = processor.process(reaction)
    assert reaction.reaction_transform is not None
    reaction = rc_extractor.extract_rc(reaction)
    rc1 = reaction.get_reaction_center_by_type(ReactionCenterType.RC1)
    assert (
        reaction.is_tautomerization_reaction
    ), f"Expected tautomerization: RC1 = {rc1.reaction_center_smiles!r}"
    # No functional groups should be found for tautomerization reactions
    assert np.array_equal(rc1.fg_signature, zero_fg_signature)


# =============================================================================
# Fixture-based tests (reaction_centers_fixtures.json)
# =============================================================================

with open(REACTION_CENTERS_FIXTURES_PATH, "r", encoding="utf-8") as _f:
    _FIXTURES_RAW = json.load(_f)


@pytest.mark.parametrize(
    "fixture",
    _FIXTURES_RAW,
    ids=[fixture["id"] for fixture in _FIXTURES_RAW],
)
def test_fixture_extraction_and_fg_annotation(
    fixture: dict,
    rc_extractor: ReactionCenterExtractor,
) -> None:
    """For each fixture: extraction runs, RCs present;
    for non-tautomerization, FG are found."""
    mapped = fixture["mapped_reaction_smiles"]
    T = ReactionTransform.from_reaction_smiles(mapped)
    reaction = Reaction(
        reaction_smiles=mapped,
        mapped_reaction_smiles=mapped,
        processed_reaction_smiles=mapped,
        reaction_transform=T,
    )
    reaction = rc_extractor.extract_rc(reaction)

    assert (
        len(reaction.reaction_centers) >= 1
    ), f"fixture id={fixture['id']}: expected at least one RC"
    if reaction.is_tautomerization_reaction:
        return
    any_fg = any(rc.fg_signature.any() for rc in reaction.reaction_centers.values())

    # These fixtures are known to have no functional groups
    if fixture["id"] not in (11, 22, 24):
        assert any_fg, (
            f"fixture id={fixture['id']}: expected at"
            f"least one RC with non-zero fg_signature"
        )


# =============================================================================
# extract_rc_for_batch
# =============================================================================


@pytest.fixture
def batch_for_extract(processor: ReactionProcessor) -> list[Reaction]:
    """Two processed reactions (with transform) and SENTINEL."""
    mapped1 = _FIXTURES_RAW[0]["mapped_reaction_smiles"]
    mapped2 = _FIXTURES_RAW[1]["mapped_reaction_smiles"]
    r1 = processor.process(Reaction(reaction_smiles=mapped1))
    r2 = processor.process(Reaction(reaction_smiles=mapped2))
    return [r1, r2, SENTINEL]


def test_extract_rc_for_batch_preserves_length_and_sentinel(
    rc_extractor: ReactionCenterExtractor,
    batch_for_extract: list[Reaction],
) -> None:
    """extract_rc_for_batch returns same length; sentinels passed through."""
    results = rc_extractor.extract_rc_for_batch(batch_for_extract)
    assert len(results) == len(batch_for_extract)
    assert not results[0].dummy
    assert not results[1].dummy
    assert results[2].dummy
    assert results[2] is SENTINEL
    assert len(results[0].reaction_centers) >= 1
    assert len(results[1].reaction_centers) >= 1


def test_extract_rc_for_batch_failure_replaced_with_sentinel(
    rc_extractor: ReactionCenterExtractor,
) -> None:
    """When extract_rc raises (e.g. no transform), that item becomes SENTINEL."""
    reaction_no_transform = Reaction(
        reaction_smiles="[CH3:1][OH:2]>>[CH3:1][O-:2]",
        reaction_transform=None,
    )
    batch = [reaction_no_transform, SENTINEL]
    results = rc_extractor.extract_rc_for_batch(batch)
    assert len(results) == 2
    assert results[0] is SENTINEL
    assert results[1] is SENTINEL


def test_extract_rc_for_batch_mixed_only_failure_replaced(
    rc_extractor: ReactionCenterExtractor,
    batch_for_extract: list[Reaction],
) -> None:
    """In a mixed batch, only the failing item becomes SENTINEL;
    order preserved."""
    valid1, valid2, sentinel = (
        batch_for_extract[0],
        batch_for_extract[1],
        batch_for_extract[2],
    )
    no_transform = Reaction(
        reaction_smiles="X>>Y",
        reaction_transform=None,
    )
    batch = [valid1, no_transform, valid2, sentinel]
    results = rc_extractor.extract_rc_for_batch(batch)
    assert len(results) == 4
    assert not results[0].dummy and len(results[0].reaction_centers) >= 1
    assert results[1] is SENTINEL
    assert not results[2].dummy and len(results[2].reaction_centers) >= 1
    assert results[3] is SENTINEL


# =============================================================================
# SEAr reactions – signatures include both GENERAL and SEAR bits (CM-3335)
# =============================================================================


def test_sear_reaction_has_general_and_sear_fg_bits(
    processor: ReactionProcessor,
    rc_extractor: ReactionCenterExtractor,
) -> None:
    """SEAr reaction signature must contain bits from both FG_COLLECTION_GENERAL
    and FG_COLLECTION_SEAR."""
    smiles = (
        "COC(C(C#CCC(OC)=O)=C1)=CC2=C1C=CC=C2.BrBr"
        ">>"
        "COC(C(C#CCC(OC)=O)=C3)=CC4=C3C=CC(Br)=C4"
    )
    reaction = Reaction(reaction_smiles=smiles)
    reaction = processor.process(reaction)
    assert reaction.is_sear_reaction

    reaction = rc_extractor.extract_rc(reaction)
    rc1 = reaction.get_reaction_center_by_type(ReactionCenterType.RC1)

    from chemcensor.rules import FG_COLLECTION_GENERAL, FG_COLLECTION_SEAR

    general_indices = {fg.idx for fg in FG_COLLECTION_GENERAL.known_groups}
    sear_indices = {fg.idx for fg in FG_COLLECTION_SEAR.known_groups}

    nonzero = set(rc1.fg_signature.nonzero()[0].tolist())
    general_hits = nonzero & general_indices
    sear_hits = nonzero & sear_indices

    assert len(general_hits) > 0, "Expected non-zero bits from FG_COLLECTION_GENERAL"
    assert len(sear_hits) > 0, "Expected non-zero bits from FG_COLLECTION_SEAR"
    assert nonzero == {58, 112, 154, 157, 160, 163, 219, 257, 515}


def test_sear_signature_collected_by_first_index_of_pattern(
    processor: ReactionProcessor,
    rc_extractor: ReactionCenterExtractor,
) -> None:
    """check one reaction in which doesn't have specific SEAr bit in the signature
    of the reaction but have it in the signature of the reaction center
    """
    smiles1 = (
        "BrBr.CC1CN(CC1NC(OC(C)(C)C)=O)c(ccc2)n3c2cnc3"
        ">>"
        "CC4CN(CC4NC(OC(C)(C)C)=O)c(ccc5Br)n6c5cnc6"
    )
    reaction = Reaction(reaction_smiles=smiles1)
    reaction = processor.process(reaction)
    assert reaction.is_sear_reaction

    reaction = rc_extractor.extract_rc(reaction)
    rc1 = reaction.get_reaction_center_by_type(ReactionCenterType.RC1)

    nonzero_center = set(rc1.fg_signature.nonzero()[0].tolist())
    assert 165 in nonzero_center

    nonzero_reaction = set(reaction.sear_signature.nonzero()[0].tolist())
    assert 11 not in nonzero_reaction
    assert 9 in nonzero_reaction


# =============================================================================
# Large molecules – symmetric expansion skip (CM-3307)
# =============================================================================

LARGE_REACTION_SMILES: list[str] = [
    (
        "CC(C)[Si](C(C)C)(C(C)C)[O:20][C@@H:19]1[C@@H:16]([CH2:17][OH:18])"
        "[O:15][C@H:14]([C:13]#[C:12][c:11]2[cH:10][cH:9][c:8]([C:7]#[C:6]"
        "[C@H:5]3[O:4][C@H:3]([CH2:2][OH:1])[C@@H:31]([O:32][Si](C(C)C)"
        "(C(C)C)C(C)C)[C@H:29]([O:30][Si](C(C)C)(C(C)C)C(C)C)[C@@H:27]3"
        "[O:28][Si](C(C)C)(C(C)C)C(C)C)[cH:26][cH:25]2)[C@@H:23]([O:24]"
        "[Si](C(C)C)(C(C)C)C(C)C)[C@H:21]1[O:22][Si](C(C)C)(C(C)C)C(C)C>>"
        "[OH:1][CH2:2][C@H:3]1[O:4][C@H:5]([C:6]#[C:7][c:8]2[cH:9][cH:10]"
        "[c:11]([C:12]#[C:13][C@H:14]3[O:15][C@H:16]([CH2:17][OH:18])"
        "[C@@H:19]([OH:20])[C@H:21]([OH:22])[C@@H:23]3[OH:24])[cH:25]"
        "[cH:26]2)[C@@H:27]([OH:28])[C@@H:29]([OH:30])[C@@H:31]1[OH:32]"
    ),
    (
        "CC(=O)[O:6][CH:5]([CH2:4][NH:3][C:2](=[O:1])[c:9]1[c:10]([I:11])"
        "[c:12]([NH:13][C:14](=[O:15])[CH:16]2[CH2:17][CH:18]([C:19](=[O:20])"
        "[NH:21][c:22]3[c:23]([I:24])[c:25]([C:26](=[O:27])[NH:28][CH2:29]"
        "[CH:30]([O:31]C(C)=O)[CH2:32][O:33]C(C)=O)[c:34]([I:35])[c:36]"
        "([C:37](=[O:38])[NH:39][CH2:40][CH:41]([O:42]C(C)=O)[CH2:43]"
        "[O:44]C(C)=O)[c:45]3[I:46])[CH2:47][CH:48]([C:49](=[O:50])[NH:51]"
        "[c:52]3[c:53]([I:54])[c:55]([C:56](=[O:57])[NH:58][CH2:59][CH:60]"
        "([O:61]C(C)=O)[CH2:62][O:63]C(C)=O)[c:64]([I:65])[c:66]([C:67]"
        "(=[O:68])[NH:69][CH2:70][CH:71]([O:72]C(C)=O)[CH2:73][O:74]C(C)=O)"
        "[c:75]3[I:76])[CH2:77]2)[c:78]([I:79])[c:80]([C:81](=[O:82])"
        "[NH:83][CH2:84][CH:85]([O:86]C(C)=O)[CH2:87][O:88]C(C)=O)[c:89]1"
        "[I:90])[CH2:7][O:8]C(C)=O>>[O:1]=[C:2]([NH:3][CH2:4][CH:5]([OH:6])"
        "[CH2:7][OH:8])[c:9]1[c:10]([I:11])[c:12]([NH:13][C:14](=[O:15])"
        "[CH:16]2[CH2:17][CH:18]([C:19](=[O:20])[NH:21][c:22]3[c:23]([I:24])"
        "[c:25]([C:26](=[O:27])[NH:28][CH2:29][CH:30]([OH:31])[CH2:32]"
        "[OH:33])[c:34]([I:35])[c:36]([C:37](=[O:38])[NH:39][CH2:40][CH:41]"
        "([OH:42])[CH2:43][OH:44])[c:45]3[I:46])[CH2:47][CH:48]([C:49]"
        "(=[O:50])[NH:51][c:52]3[c:53]([I:54])[c:55]([C:56](=[O:57])[NH:58]"
        "[CH2:59][CH:60]([OH:61])[CH2:62][OH:63])[c:64]([I:65])[c:66]"
        "([C:67](=[O:68])[NH:69][CH2:70][CH:71]([OH:72])[CH2:73][OH:74])"
        "[c:75]3[I:76])[CH2:77]2)[c:78]([I:79])[c:80]([C:81](=[O:82])"
        "[NH:83][CH2:84][CH:85]([OH:86])[CH2:87][OH:88])[c:89]1[I:90]"
    ),
]


@pytest.mark.parametrize(
    "processed_smiles",
    LARGE_REACTION_SMILES,
    ids=["sugar_TIPS_deprotection", "macrocyclic_deacetylation"],
)
def test_large_molecules_do_not_hang(
    processed_smiles: str,
    rc_extractor: ReactionCenterExtractor,
) -> None:
    """Reactions with many reaction center fragments should finish quickly
    by skipping symmetric expansion (previously caused infinite hang)."""
    T = ReactionTransform.from_reaction_smiles(processed_smiles)
    reaction = Reaction(
        reaction_smiles=processed_smiles,
        mapped_reaction_smiles=processed_smiles,
        processed_reaction_smiles=processed_smiles,
        reaction_transform=T,
    )
    reaction = rc_extractor.extract_rc(reaction)
    assert len(reaction.reaction_centers) >= 1


# =============================================================================
# Symmetric reactant expansion (para-disubstituted amine)
# =============================================================================


def test_symmetric_para_amine_doubles_rc1_second_reactant_index_count(
    processor: ReactionProcessor,
    rc_extractor: ReactionCenterExtractor,
) -> None:
    """Mesylation on one C-NH-C arm of a para-symmetric diamine.

    For RC1, ``reactant_fragments[1]`` is the fragment on the symmetric
    reactant; symmetric expansion duplicates indices on the equivalent arm, so
    ``len(reactant_indices[1])`` is twice ``fr_mol.GetNumAtoms()`` for that
    fragment.
    """
    smiles = "CNCC1=CC=C(CNC)C=C1.CC(OS(C)(=O)=O)C>>CN(C(C)C)CC2=CC=C(CNC)C=C2"
    reaction = Reaction(reaction_smiles=smiles)
    reaction = processor.process(reaction)
    reaction = rc_extractor.extract_rc(reaction)

    rc1 = reaction.get_reaction_center_by_type(ReactionCenterType.RC1)
    frag = rc1.reactant_fragments[1]
    indices = rc1.reactant_indices[1]

    assert len(indices) == 2 * frag.fr_mol.GetNumAtoms()


def test_symmetric_reductive_amination(
    processor: ReactionProcessor,
    rc_extractor: ReactionCenterExtractor,
) -> None:
    """Symmetric reductive amination. Aldehyde shouldn't
    be included in the signature.
    """
    smiles = "NC1=CC=C(N(C)C)C=C1.O=CCC=O>>O=CCCNC1=CC=C(N(C)C)C=C1"
    reaction = Reaction(reaction_smiles=smiles)
    reaction = processor.process(reaction)
    reaction = rc_extractor.extract_rc(reaction)

    rc1 = reaction.get_reaction_center_by_type(ReactionCenterType.RC1)

    assert rc1.fg_signature[87] == 0  # Aldehyde [Ch]=[O]


def test_symmetric_biphenyl_case_RC2(
    processor: ReactionProcessor,
    rc_extractor: ReactionCenterExtractor,
) -> None:
    """SNAr reaction with symmetric biphenyl reactant.

    For RC2, ``reactant_fragments[1]`` is the fragment on the symmetric
    reactant; symmetric expansion duplicates indices on the equivalent ring, so
    ``len(reactant_indices[1])`` is twice ``fr_mol.GetNumAtoms()`` for that
    fragment.
    """
    smiles = (
        "CC(OC(NC(Cc1ccnc(Cl)c1)C(OC(C)(C)C)=O)=O)(C)C.Oc2ccccc2c3ccccc3O"
        ">>"
        "CC(OC(NC(Cc4ccnc(Oc5ccccc5c6ccccc6O)c4)C(OC(C)(C)C)=O)=O)(C)C"
    )
    reaction = Reaction(reaction_smiles=smiles)
    reaction = processor.process(reaction)
    reaction = rc_extractor.extract_rc(reaction)

    rc2 = reaction.get_reaction_center_by_type(ReactionCenterType.RC2)
    frag = rc2.reactant_fragments[1]
    indices = rc2.reactant_indices[1]

    assert len(indices) == 2 * frag.fr_mol.GetNumAtoms()


# =============================================================================
# Exception tests
# =============================================================================


def test_extract_and_annotate_raises_when_no_transform(
    rc_extractor: ReactionCenterExtractor,
) -> None:
    """extract_and_annotate_rcs raises ReactionCenterExtractorError (wrapping
    MissingReactionTransformError) when reaction has no transform."""
    reaction = Reaction(
        reaction_smiles="[CH3:1][OH:2]>>[CH3:1][O-:2]",
        reaction_transform=None,
    )
    with pytest.raises(ReactionCenterExtractorError) as exc_info:
        rc_extractor.extract_rc(reaction)
    assert isinstance(exc_info.value.__cause__, MissingReactionTransformError)


def test_extract_rc_raises_when_reacting_atoms_not_set(
    processor: ReactionProcessor,
    rc_extractor: ReactionCenterExtractor,
) -> None:
    """extract_rc raises ReactionCenterExtractorError (wrapping
    MissingReactingAtomsError) when reacting atoms are not set on the
    transform after processing."""
    smiles = (
        "C[N+](C)(C)CCOP(=O)([O-])OCCCCCCCCCCCCCCCCCCc1ccc(I)cc1"
        ".[131I][131I]"
        ">>"
        "C[N+](C)(C)CCOP(=O)([O-])OCCCCCCCCCCCCCCCCCCc1ccc([131I])cc1"
    )
    reaction = Reaction(reaction_smiles=smiles)
    reaction = processor.process(reaction)
    with pytest.raises(
        ReactionCenterExtractorError,
        match=(
            r"Reaction center extraction has failed: "
            r"Reacting atoms are not set on the transform\. "
            r"Cannot extract reaction center\."
        ),
    ) as exc_info:
        rc_extractor.extract_rc(reaction)
    assert isinstance(exc_info.value.__cause__, MissingReactingAtomsError)


# test updated linear configs
def test_linear_configs_include_chiral(
    processor: ReactionProcessor,
    rc_extractor: ReactionCenterExtractor,
) -> None:
    """Linear configs should include chiral centers' neighbors."""
    smiles = (
        "CC(C)(C)OC(=O)CN1CCC[C@H]1C(=O)Nc1csc(Nc2cccc3[nH]ccc23)n1"
        ">>"
        "O=C(O)CN1CCC[C@H]1C(=O)Nc1csc(Nc2cccc3[nH]ccc23)n1"
    )
    reaction = Reaction(reaction_smiles=smiles)
    reaction = processor.process(reaction)

    reaction = rc_extractor.extract_rc(reaction)
    rc4 = reaction.get_reaction_center_by_type(ReactionCenterType.RC4)

    assert rc4.reaction_center_smiles == (
        "CC(C)(C)OC(=O)CN1CCC[C@H]1C=O>" ">OC(=O)CN1CCC[C@H]1C=O"
    )

    smiles2 = (
        "Cc1cc(-n2cc(C[C@H](C)C(=O)OC(C)(C)C)c3nccnc32)cc(C2CC2)c1NC(=O)C[C@H]1CCNC1"
        ">>"
        "Cc1cc(-n2cc(C[C@H](C)C(=O)O)c3nccnc32)cc(C2CC2)c1NC(=O)C[C@H]1CCNC1"
    )
    reaction2 = Reaction(reaction_smiles=smiles2)
    reaction2 = processor.process(reaction2)

    reaction2 = rc_extractor.extract_rc(reaction2)
    rc3 = reaction2.get_reaction_center_by_type(ReactionCenterType.RC4)
    assert rc3.reaction_center_smiles == "cC[C@H](C)C(=O)OC(C)(C)C>>cC[C@H](C)C(O)=O"


# =============================================================================
# Spectator ions: RC SMILES uses light-atom forms (N, O), not [NH4], [OH]
# =============================================================================

_REACTION_AMMONIUM_DECARBOXYLATION = (
    "COCCCN1CCOc2ccc(CO[C@H]3CN(S(=O)(=O)c4ccc(C)cc4)[C@H](CC(C)(C)C(=O)O)"
    "C[C@@H]3c3ccc(OC)cc3)cc21.[NH4+]>>"
    "COCCCN1CCOc2ccc(CO[C@H]3CN(S(=O)(=O)c4ccc(C)cc4)[C@H](CC(C)(C)C#N)"
    "C[C@@H]3c3ccc(OC)cc3)cc21"
)

_REACTION_AMIDATION_WITH_HYDROXIDE = (
    "Brc1ccccn1.N#Cc1ccccc1N.[OH-]>>Nc1ccccc1C(=O)c1ccccn1"
)


def test_reaction_center_smiles_ammonium_spectator_is_n_not_bracket_nh4(
    processor: ReactionProcessor,
    rc_extractor: ReactionCenterExtractor,
) -> None:
    """Unmapped ammonium in the reactant pool must not appear as ``[NH4]`` in RC1."""
    reaction = Reaction(reaction_smiles=_REACTION_AMMONIUM_DECARBOXYLATION)
    reaction = processor.process(reaction)
    reaction = rc_extractor.extract_rc(reaction)
    rc1 = reaction.get_reaction_center_by_type(ReactionCenterType.RC1)
    smiles = rc1.reaction_center_smiles
    assert "[NH4]" not in smiles
    assert ".N>>" in smiles


def test_reaction_center_smiles_hydroxide_spectator_is_o_not_bracket_oh(
    processor: ReactionProcessor,
    rc_extractor: ReactionCenterExtractor,
) -> None:
    """Unmapped hydroxide in the reactant pool must not appear as ``[OH]`` in RC1."""
    reaction = Reaction(reaction_smiles=_REACTION_AMIDATION_WITH_HYDROXIDE)
    reaction = processor.process(reaction)
    reaction = rc_extractor.extract_rc(reaction)
    rc1 = reaction.get_reaction_center_by_type(ReactionCenterType.RC1)
    smiles = rc1.reaction_center_smiles
    assert "[OH]" not in smiles
    assert smiles.startswith("O.")


def test_no_extra_hydrogens_in_rc_smiles(
    processor: ReactionProcessor,
    rc_extractor: ReactionCenterExtractor,
) -> None:
    """No extra hydrogens in the RC SMILES."""
    smiles = (
        "CS(=O)(=O)c1ccc(-c2cc[nH]c(=O)c2C[C@H]2CC[NH2+]C2)cc1.O=C(O)c1nncs1"
        ">>"
        "CS(=O)(=O)c1ccc(-c2cc[nH]c(=O)c2C[C@H]2CCN(C(=O)c3nncs3)C2)cc1"
    )
    reaction = Reaction(reaction_smiles=smiles)
    reaction = processor.process(reaction)
    reaction = rc_extractor.extract_rc(reaction)
    rc1 = reaction.get_reaction_center_by_type(ReactionCenterType.RC1)
    rc_smiles = rc1.reaction_center_smiles
    assert "H" not in rc_smiles
    assert rc_smiles == "CNC.cC(O)=O>>cC(=O)N(C)C"


def test_no_extra_hydrogens_in_static_part_of_rc_smiles(
    processor: ReactionProcessor,
    rc_extractor: ReactionCenterExtractor,
) -> None:
    """No extra hydrogens in the RC2."""
    smiles = "CC1[NH2+]CCN(CC2=CC=CC=C2)C1>>CC3[NH2+]CCNC3"
    reaction = Reaction(reaction_smiles=smiles)
    reaction = processor.process(reaction)
    reaction = rc_extractor.extract_rc(reaction)
    rc2 = reaction.get_reaction_center_by_type(ReactionCenterType.RC2)
    rc_smiles = rc2.reaction_center_smiles
    assert "H" not in rc_smiles
    assert rc_smiles == "C1CN(Cc2ccccc2)CCN1>>C1CNCCN1"
