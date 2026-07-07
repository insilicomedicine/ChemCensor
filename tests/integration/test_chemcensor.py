from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from rdkit import Chem

from chemcensor.basic import Reaction
from chemcensor.basic import ReactionCenterType
from chemcensor.chemcensor import ChemCensor
from chemcensor.chemcensor import ScoreResult
from chemcensor.configs.scoring_configs import ScoringConfig
from chemcensor.db.manager import DBManager
from chemcensor.errors import InvalidCenterTypeError
from chemcensor.extraction import ReactionCenterExtractor
from chemcensor.processing.reaction_processor import ReactionProcessor
from chemcensor.rules.functional_groups import FG_COLLECTION_SEAR
from chemcensor.rules.functional_groups import FG_SIGNATURE_LENGTH

# Paths
_THIS_DIR = Path(__file__).resolve().parent
_TESTS_DIR = _THIS_DIR.parent
FIXTURES_DIR = _THIS_DIR / "fixtures"
RC_DB_PATH = FIXTURES_DIR / "rc_db.db"
REACTION_FIXTURES_PATH = (
    _TESTS_DIR / "unit" / "extraction" / "fixtures" / "reaction_centers_fixtures.json"
)

# Must match scripts/create_test_db.py FIXTURE_GROUPS
# (max_center_type_in_db, fixture_id, ...)
FIXTURE_GROUPS: list[tuple[int, ...]] = [
    (4, 1, 2, 5, 10),  # full RC1–RC4 in DB
    (1, 17, 19),  # only RC1 in DB
    (2, 3, 4),  # RC1, RC2 in DB
    (3, 11, 14),  # RC1, RC2, RC3 in DB
]

NOT_IN_DB_FIXTURE_IDS = (6, 7, 8, 9, 12, 13)

with open(REACTION_FIXTURES_PATH, "r", encoding="utf-8") as _f:
    _FIXTURES = json.load(_f)


def _get_fixture(fixture_id: int) -> dict:
    return next(f for f in _FIXTURES if f["id"] == fixture_id)


def _strip_atom_maps(mapped_rxn_smiles: str) -> str:
    """Strip atom map numbers from a mapped reaction SMILES and canonicalize."""
    reactants_str, _, product_str = mapped_rxn_smiles.split(">")
    reactants_mol = Chem.MolFromSmiles(reactants_str)
    product_mol = Chem.MolFromSmiles(product_str)
    for atom in reactants_mol.GetAtoms():
        atom.SetAtomMapNum(0)
    for atom in product_mol.GetAtoms():
        atom.SetAtomMapNum(0)
    return f"{Chem.MolToSmiles(reactants_mol)}>>{Chem.MolToSmiles(product_mol)}"


@pytest.fixture(scope="module")
def db_path() -> Path:
    """Path to pre-built rc_db.db (create with: python scripts/create_test_db.py)."""
    if not RC_DB_PATH.exists():
        pytest.skip(
            f"rc_db.db not found at {RC_DB_PATH}; run scripts/create_test_db.py"
        )
    return RC_DB_PATH


# ---------------------------------------------------------------------------
# Score when reaction centers ARE in DB (by FIXTURE_GROUPS)
# ---------------------------------------------------------------------------


def _in_db_cases() -> list[tuple[int, int]]:
    """(fixture_id, max_center_type) for fixtures that are in rc_db.db."""
    cases: list[tuple[int, int]] = []
    for group in FIXTURE_GROUPS:
        max_in_db, *fids = group
        for fid in fids:
            # Can score with max_center_type from 1 up to max_in_db
            for requested_max in range(1, max_in_db + 1):
                cases.append((fid, requested_max))
    return cases


@pytest.mark.parametrize(
    "fixture_id,max_center_type",
    _in_db_cases(),
    ids=[f"fixture_{fid}_max{mct}" for fid, mct in _in_db_cases()],
)
def test_score_when_centers_in_db(
    fixture_id: int,
    max_center_type: int,
    db_path: Path,
) -> None:
    """Fixtures in DB have their canonical SMILES stored → exact_match_scoring."""
    fixture = _get_fixture(fixture_id)
    smiles = _strip_atom_maps(fixture["mapped_reaction_smiles"])

    censor = ChemCensor(
        db_path=db_path,
        max_center_type=max_center_type,
    )
    score = censor.score(smiles)

    assert (
        score == ScoringConfig.exact_match_scoring.value
    ), f"fixture {fixture_id}, max_center_type={max_center_type}"


# ---------------------------------------------------------------------------
# Score when reaction is NOT in DB
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fixture_id",
    NOT_IN_DB_FIXTURE_IDS,
    ids=[f"fixture_{i}" for i in NOT_IN_DB_FIXTURE_IDS],
)
def test_score_returns_default_when_fixture_not_in_db(
    fixture_id: int,
    db_path: Path,
) -> None:
    """Fixture not in rc_db.db → default_reaction_scoring."""
    fixture = _get_fixture(fixture_id)
    censor = ChemCensor(db_path=db_path)
    smiles = _strip_atom_maps(fixture["mapped_reaction_smiles"])
    score = censor.score(smiles)
    assert score == ScoringConfig.default_reaction_scoring.value


def test_score_returns_default_when_db_empty() -> None:
    """Empty DB → default_reaction_scoring."""
    fixture = _get_fixture(1)
    empty_path = FIXTURES_DIR / "empty_rc_db.db"
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    DBManager().dump(empty_path)

    censor = ChemCensor(db_path=empty_path)
    smiles = _strip_atom_maps(fixture["mapped_reaction_smiles"])
    score = censor.score(smiles)

    assert score == ScoringConfig.default_reaction_scoring.value


def test_score_returns_default_when_only_unrelated_center_in_db() -> None:
    """DB with unrelated center only → default_reaction_scoring."""
    fixture = _get_fixture(1)
    db = DBManager()
    db.add_reaction_center(
        "other>>center", np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
    )
    other_path = FIXTURES_DIR / "other_rc_db.db"
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    db.dump(other_path)

    censor = ChemCensor(db_path=other_path)
    smiles = _strip_atom_maps(fixture["mapped_reaction_smiles"])
    score = censor.score(smiles)

    assert score == ScoringConfig.default_reaction_scoring.value


# ---------------------------------------------------------------------------
# check_functional_groups flag: center present in DB but FG signature differs
# ---------------------------------------------------------------------------

# Fixture 19 (an aryl C–N coupling) with an extra nitro group grafted onto the
# remote ester arm. The reaction center (CNC.cc(c)Cl>>CN(C)c(c)c) is unchanged,
# so it still matches the DB entry built from the original fixture, but the
# added functional group makes the RC1 FG sub-signature no longer a subset of
# the stored reference.
FIXTURE_19_WITH_EXTRA_FG_RXN_SMILES = (
    "CC([N+]([O-])=O)OC([C@@H]1CCNC[C@@H]1OC2CCCCO2)=O."
    "FC(F)(c(cc3n4nccc4)nc5c3cc(Cl)cc5)F>>"
    "CC([N+]([O-])=O)OC([C@@H]6CCN(C[C@@H]6OC7CCCCO7)c(cc8)cc9c8nc(C(F)(F)F)"
    "cc9n%10nccc%10)=O"
)


def test_score_center_in_db_with_nonmatching_fg() -> None:
    """A center present in the DB but with a non-matching FG sub-signature.

    The DB stores fixture 19's real RC1 center and its real FG signature. We
    then score a variant of the same reaction with an extra functional group
    (a nitro group on a remote arm): the reaction center is identical, so it is
    found in the DB, but its FG sub-signature now contains a bit absent from the
    stored reference.

    With ``check_functional_groups=True`` (default) the center does not count
    and scoring falls back to ``default_reaction_scoring``. With the flag set to
    ``False`` the center is scored on DB presence alone → ``lc_1_scoring``.
    """
    original_smiles = _strip_atom_maps(_get_fixture(19)["mapped_reaction_smiles"])

    # Build the DB from the ORIGINAL reaction: store its RC1 center together with
    # its genuine FG signature (no artificial zeroing).
    original = ReactionProcessor().process(Reaction(reaction_smiles=original_smiles))
    original = ReactionCenterExtractor(
        max_center_type=ReactionCenterType.RC1
    ).extract_rc(original)
    original_rc1 = original.reaction_centers[ReactionCenterType.RC1]

    db = DBManager()
    db.add_reaction_center(
        original_rc1.reaction_center_smiles,
        original_rc1.fg_signature,
    )

    modified_smiles = FIXTURE_19_WITH_EXTRA_FG_RXN_SMILES

    with_fg_check = ChemCensor(
        manager=db,
        max_center_type=1,
        find_exact_match=False,
        check_functional_groups=True,
    )
    assert (
        with_fg_check.score(modified_smiles)
        == ScoringConfig.default_reaction_scoring.value
    )

    without_fg_check = ChemCensor(
        manager=db,
        max_center_type=1,
        find_exact_match=False,
        check_functional_groups=False,
    )
    assert without_fg_check.score(modified_smiles) == ScoringConfig.lc_1_scoring.value


# ---------------------------------------------------------------------------
# evaluate() / ScoreResult: both FG variants in a single pass
# ---------------------------------------------------------------------------


def test_score_result_uniform_and_select() -> None:
    """``ScoreResult.uniform`` sets both variants; ``select`` picks one."""
    uniform = ScoreResult.uniform(3.0)
    assert uniform.with_functional_groups == 3.0
    assert uniform.without_functional_groups == 3.0

    result = ScoreResult(with_functional_groups=0.0, without_functional_groups=1.0)
    assert result.select(check_functional_groups=True) == 0.0
    assert result.select(check_functional_groups=False) == 1.0


def test_evaluate_returns_uniform_for_exact_match(db_path: Path) -> None:
    """A reaction in the DB scores ``exact_match`` for both variants."""
    smiles = _strip_atom_maps(_get_fixture(1)["mapped_reaction_smiles"])
    censor = ChemCensor(db_path=db_path)

    result = censor.evaluate(smiles)

    expected = ScoringConfig.exact_match_scoring.value
    assert result == ScoreResult.uniform(expected)


def test_evaluate_returns_uniform_for_failed_reaction(db_path: Path) -> None:
    """An unprocessable reaction scores ``failed`` for both variants."""
    censor = ChemCensor(db_path=db_path)

    result = censor.evaluate("not-a-reaction")

    failed = ScoringConfig.failed_reaction_scoring.value
    assert result == ScoreResult.uniform(failed)


def test_evaluate_distinguishes_fg_variants_in_single_pass() -> None:
    """``evaluate`` returns differing scores when the FG sub-signature fails.

    Same setup as :func:`test_score_center_in_db_with_nonmatching_fg`: the DB
    holds fixture 19's RC1 center with its genuine FG signature, and we score a
    variant carrying an extra functional group. A single ``evaluate`` call must
    report ``default`` with the FG check and ``lc_1`` without it.
    """
    original_smiles = _strip_atom_maps(_get_fixture(19)["mapped_reaction_smiles"])
    original = ReactionProcessor().process(Reaction(reaction_smiles=original_smiles))
    original = ReactionCenterExtractor(
        max_center_type=ReactionCenterType.RC1
    ).extract_rc(original)
    original_rc1 = original.reaction_centers[ReactionCenterType.RC1]

    db = DBManager()
    db.add_reaction_center(
        original_rc1.reaction_center_smiles,
        original_rc1.fg_signature,
    )

    censor = ChemCensor(manager=db, max_center_type=1, find_exact_match=False)
    result = censor.evaluate(FIXTURE_19_WITH_EXTRA_FG_RXN_SMILES)

    assert result == ScoreResult(
        with_functional_groups=ScoringConfig.default_reaction_scoring.value,
        without_functional_groups=ScoringConfig.lc_1_scoring.value,
    )


@pytest.mark.parametrize("check_functional_groups", [True, False])
def test_evaluate_select_matches_score(
    db_path: Path, check_functional_groups: bool
) -> None:
    """``evaluate(...).select(flag)`` equals ``score`` of a censor with that flag.

    Verified across an in-DB fixture, an out-of-DB fixture and a failed
    reaction so both early-exit and per-center paths are covered.
    """
    smiles_inputs = [
        _strip_atom_maps(_get_fixture(1)["mapped_reaction_smiles"]),
        _strip_atom_maps(_get_fixture(6)["mapped_reaction_smiles"]),
        "not-a-reaction",
    ]
    censor = ChemCensor(
        db_path=db_path, check_functional_groups=check_functional_groups
    )

    for smiles in smiles_inputs:
        assert censor.evaluate(smiles).select(check_functional_groups) == censor.score(
            smiles
        )


# ---------------------------------------------------------------------------
# RC1-only in DB: fixtures 17, 19 → lc_1 when find_exact_match=False
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("fixture_id", (17, 19), ids=["fixture_17", "fixture_19"])
def test_score_rc1_only_in_db_returns_lc_1(
    fixture_id: int,
    db_path: Path,
) -> None:
    """Fixtures 17, 19: only RC1 in DB, exact match off → lc_1_scoring."""
    fixture = _get_fixture(fixture_id)
    censor = ChemCensor(
        db_path=db_path,
        find_exact_match=False,
    )
    smiles = _strip_atom_maps(fixture["mapped_reaction_smiles"])
    score = censor.score(smiles)
    assert score == ScoringConfig.lc_1_scoring.value


# ---------------------------------------------------------------------------
# Exact match scoring (find_exact_match=True)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("fixture_id", (17, 19), ids=["fixture_17", "fixture_19"])
def test_score_exact_match(
    fixture_id: int,
    db_path: Path,
) -> None:
    """Fixtures in DB with find_exact_match=True → exact_match_scoring."""
    fixture = _get_fixture(fixture_id)
    censor = ChemCensor(db_path=db_path)
    smiles = _strip_atom_maps(fixture["mapped_reaction_smiles"])
    score = censor.score(smiles)
    assert score == ScoringConfig.exact_match_scoring.value


# ---------------------------------------------------------------------------
# Invalid max_center_type
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("bad_value", [0, 5, -1, 99])
def test_raises_on_invalid_center_type(
    db_path: Path,
    bad_value: int,
) -> None:
    """Invalid max_center_type raises InvalidCenterTypeError on init."""
    with pytest.raises(InvalidCenterTypeError, match=str(bad_value)):
        ChemCensor(db_path=db_path, max_center_type=bad_value)


# ---------------------------------------------------------------------------
# Failed processing
# ---------------------------------------------------------------------------


def test_score_returns_failed_when_processing_fails(
    db_path: Path,
) -> None:
    """Invalid reaction (e.g. empty) → failed_reaction_scoring."""
    censor = ChemCensor(db_path=db_path, max_center_type=1)
    assert censor.score(">>") == ScoringConfig.failed_reaction_scoring.value


def test_score_returns_failed_for_bad_smiles(
    db_path: Path,
) -> None:
    """Invalid SMILES → failed_reaction_scoring."""
    censor = ChemCensor(db_path=db_path, max_center_type=1)
    assert censor.score("not-a-reaction") == ScoringConfig.failed_reaction_scoring.value


# ---------------------------------------------------------------------------
# SIS reaction scoring
# ---------------------------------------------------------------------------

SIS_MAPPED_SMILES = (
    "[CH3:1][C:2](=[O:3])[CH:4]1[CH2:5][C@@H:6]2[CH2:7]"
    "[CH2:8][CH2:9][C@H:10]1[CH2:11][CH2:12]2>>[CH3:1]"
    "[C:2](=[O:3])[C@H:4]1[CH2:5][C@@H:6]2[CH2:7][CH2:8]"
    "[CH2:9][C@H:10]1[CH2:11][CH2:12]2"
)


def test_score_returns_sis_scoring(db_path: Path) -> None:
    """SIS reaction → sis_reaction_scoring."""
    smiles = _strip_atom_maps(SIS_MAPPED_SMILES)
    censor = ChemCensor(db_path=db_path)
    score = censor.score(smiles)
    assert score == ScoringConfig.sis_reaction_scoring.value


# Unmapped SMILES: Mapper + full pipeline (same as production)
DOUBLE_BOND_INVERSION_RXN_SMILES = (
    r"CC#N.Cc1oc(-c2ccccc2)nc1CCOc1ccc(/C=C2\SC(=O)NC2=O)cc1>>"
    r"Cc1oc(-c2ccccc2)nc1CCOc1ccc(/C=C2/SC(=O)NC2=O)cc1"
)

ALKENE_STEREORESOLUTION_RXN_SMILES = (
    r"CC(=Cc1ccc(C(=O)O)cc1)c1ccc(O)c(C(C)(C)C)c1.CCCCCC.CCOCC.CN(C)C=O.C[S-].[Li+]>>"
    r"C/C(=C\c1ccc(C(=O)O)cc1)c1ccc(O)c(C(C)(C)C)c1"
)

STEREO_ISSUE_NONFAILED_BASELINE_SMILES = (
    "CN(Cc1ccccc1)C[C@H](CN=[N+]=[N-])NC(=O)OC(C)(C)C>>CNC[C@H](CN)NC(=O)OC(C)(C)C",
    "CN(Cc1ccccc1)C[C@H](CN=[N+]=[N-])NC(=O)OC(C)(C)C.O=C(OC(Cl)(Cl)Cl)OC(Cl)(Cl)Cl>>"
    "CN1C[C@@H](NC(=O)OC(C)(C)C)CNC1=O",
    (
        "COc1ccc(-n2ncc3c(C4CC4)cc(O)nc32)nc1."
        "C[C@H]1C[C@H]([O+]=P(c2ccccc2)(c2ccccc2)c2ccccc2)C1>>"
        "COc1ccc(-n2ncc3c(C4CC4)cc(O[C@@H]4C[C@H](C)C4)nc32)nc1"
    ),
    "COc1ccc(-n2ncc3c(C4CC4)cc(O)nc32)nc1.C[C@H]1C[C@H](O)C1>>"
    "COc1ccc(-n2ncc3c(C4CC4)cc(O[C@@H]4C[C@H](C)C4)nc32)nc1",
    (
        "COc1ccc(-n2ncc3c(C4CC4)cc(Br)nc32)nc1."
        "C[C@H]1C[C@H]([O+]=P(c2ccccc2)(c2ccccc2)c2ccccc2)C1>>"
        "COc1ccc(-n2ncc3c(C4CC4)cc(O[C@@H]4C[C@H](C)C4)nc32)nc1"
    ),
    "C[C@H]1C[C@@H](Br)C1.O=[N+]([O-])c1ccc(C[O][Na])cc1>>"
    "C[C@H]1C[C@H](OCc2ccc([N+](=O)[O-])cc2)C1",
    "C[C@H]1C[C@@H](Br)C1.O=[N+]([O-])c1ccc(CO)cc1>>"
    "C[C@H]1C[C@H](OCc2ccc([N+](=O)[O-])cc2)C1",
    "CO.C[C@H]1C[C@@H](Br)C1>>C[C@H]1C[C@H](O)C1",
    "CCc1csc(N)n1.O=C(O)[C@H]1C[C@H](O)C1>>CCc1csc(N[C@@H]2C[C@H](C(=O)O)C2)n1",
    (
        "CCB1OC(C)(C)C(C)(C)O1.Nc1nc(Br)cs1."
        "O=C(O)[C@@H]1C[C@@H]([O+]=P(c2ccccc2)(c2ccccc2)c2ccccc2)C1>>"
        "CCc1csc(N[C@@H]2C[C@H](C(=O)O)C2)n1"
    ),
    "CCc1csc(N)n1.O=C(O)[C@@H]1C[C@@H]([O+]=P(c2ccccc2)(c2ccccc2)c2ccccc2)C1>>"
    "CCc1csc(N[C@@H]2C[C@H](C(=O)O)C2)n1",
)

STEREO_ISSUE_NONFAILED_SIS_SMILES = (
    "NC(Cc1ccnc(Oc2ccccc2-c2ccccc2-c2ccc(=O)n([C@@H]3C[C@H](F)C3)c2)c1)C(=O)O>>"
    "N[C@@H](Cc1ccnc(Oc2ccccc2-c2ccccc2-c2ccc(=O)n([C@@H]3C[C@H](F)C3)c2)c1)C(=O)O",
)

STEREO_ISSUE_NONFAILED_PSEUDO_TO_ASYMMETRIC_SMILES = (
    (
        "N[C@@H](Cc1ccnc(Oc2ccccc2-c2ccccc2B(O)O)c1)C(=O)O."
        "O=c1ccc(Br)cn1[C@@H]1C[C@H](F)C1>>"
        "N[C@@H](Cc1ccnc(Oc2ccccc2-c2ccccc2-c2ccc(=O)n([C@@H]3C[C@H](F)C3)c2)c1)"
        "C(=O)O"
    ),
    "N[C@@H](Cc1ccnc(Oc2ccccc2-c2ccccc2Br)c1)C(=O)O.O=c1ccc(Br)cn1[C@@H]1C[C@H](F)C1>>"
    "N[C@@H](Cc1ccnc(Oc2ccccc2-c2ccccc2-c2ccc(=O)n([C@@H]3C[C@H](F)C3)c2)c1)C(=O)O",
)

STEREO_ISSUE_FAILED_SCORE_SMILES = (
    (
        "CC1(C)OB(c2ccc(=O)n([C@@H]3C[C@H](F)C3)c2)OC1(C)C."
        "NC(Cc1ccnc(Oc2ccccc2-c2ccccc2Br)c1)C(=O)O>>"
        "N[C@@H](Cc1ccnc(Oc2ccccc2-c2ccccc2-c2ccc(=O)n([C@@H]3C[C@H](F)C3)c2)c1)"
        "C(=O)O"
    ),
)


@pytest.fixture(
    scope="module",
    params=STEREO_ISSUE_NONFAILED_BASELINE_SMILES,
    ids=[str(i) for i, _ in enumerate(STEREO_ISSUE_NONFAILED_BASELINE_SMILES, 1)],
)
def stereo_issue_nonfailed_baseline_smiles(request: pytest.FixtureRequest) -> str:
    """Stereo regressions that should score successfully."""
    return request.param


@pytest.fixture(
    scope="module",
    params=STEREO_ISSUE_NONFAILED_SIS_SMILES,
    ids=[str(i) for i, _ in enumerate(STEREO_ISSUE_NONFAILED_SIS_SMILES, 1)],
)
def stereo_issue_nonfailed_sis_smiles(request: pytest.FixtureRequest) -> str:
    """Pure no-edit ``? -> R/S`` regressions that should be classified as SIS."""
    return request.param


@pytest.fixture(
    scope="module",
    params=STEREO_ISSUE_NONFAILED_PSEUDO_TO_ASYMMETRIC_SMILES,
    ids=[
        str(i)
        for i, _ in enumerate(STEREO_ISSUE_NONFAILED_PSEUDO_TO_ASYMMETRIC_SMILES, 1)
    ],
)
def stereo_issue_nonfailed_pseudo_to_asymmetric_smiles(
    request: pytest.FixtureRequest,
) -> str:
    """Dynamic reactions where reactant ``r/s`` becomes ordinary ``R/S``."""
    return request.param


@pytest.fixture(
    scope="module",
    params=STEREO_ISSUE_FAILED_SCORE_SMILES,
    ids=[str(i) for i, _ in enumerate(STEREO_ISSUE_FAILED_SCORE_SMILES, 1)],
)
def stereo_issue_failed_score_smiles(request: pytest.FixtureRequest) -> str:
    """Regression reactions that should still return the failed score."""
    return request.param


def test_score_returns_failed_for_double_bond_inversion_not_sis(
    db_path: Path,
) -> None:
    """E/Z inversion on an already-specified alkene (not SIS) →
    inconsistent static stereo → failed."""
    censor = ChemCensor(db_path=db_path)
    score = censor.score(DOUBLE_BOND_INVERSION_RXN_SMILES)
    assert score == ScoringConfig.failed_reaction_scoring.value


def test_score_returns_sis_for_alkene_stereoresolution(db_path: Path) -> None:
    """Unmapped mixture; OrphanRemover + E/Z SIS on alkene → sis_reaction_scoring."""
    censor = ChemCensor(db_path=db_path)
    score = censor.score(ALKENE_STEREORESOLUTION_RXN_SMILES)
    assert score == ScoringConfig.sis_reaction_scoring.value


# R/S SIS, ``p_reacting_atoms`` empty; canonical atom order differs between R and P
# (SIS detection must pair atoms via ``pR_map`` indices — otherwise extraction runs).
SIS_ATOM_RXN_MULTIFRAG_B = (
    "CC(C)S(=O)(=O)NC[C@@H](C)Oc1ccc(Br)cc1."
    "CC(CNS(=O)(=O)C(C)C)Oc1ccc(-c2ccc(C#N)cc2)cc1."
    "CC(O)C(C)O.O=C([O-])[O-].[Na+]."
    "c1ccc([P](c2ccccc2)(c2ccccc2)[Pd]([P](c2ccccc2)(c2ccccc2)c2ccccc2)"
    "([P](c2ccccc2)(c2ccccc2)c2ccccc2)[P](c2ccccc2)(c2ccccc2)c2ccccc2)cc1>>"
    "CC(C)S(=O)(=O)NC[C@@H](C)Oc1ccc(-c2ccc(C#N)cc2)cc1"
)
# One center ?→R; other R centers keep same R/S label (CW/CCW may still differ
# in RDKit after canonicalization — SIS uses R/S labels, not GetChiralTag).
SIS_ATOM_RXN_POLYCYCLE = (
    "CC(O)c1ccc2c(n1)N1[C@H](C2)CN(C(=O)OC(C)(C)C)C[C@H]1C.ClCCl.O=C(O)C(F)(F)F>>"
    "C[C@@H]1CN(C(=O)OC(C)(C)C)C[C@H]2Cc3ccc([C@@H](C)O)nc3N21"
)


@pytest.mark.parametrize(
    "reaction_smiles",
    [SIS_ATOM_RXN_MULTIFRAG_B, SIS_ATOM_RXN_POLYCYCLE],
    ids=["multifrag_suzuki_like", "polycycle_rs_only"],
)
def test_score_returns_sis_for_atom_stereo_mapped_order(
    db_path: Path,
    reaction_smiles: str,
) -> None:
    """Atom SIS when product/reactant indices differ under canonicalization →
    SIS score."""
    censor = ChemCensor(db_path=db_path)
    assert censor.score(reaction_smiles) == ScoringConfig.sis_reaction_scoring.value


def test_score_does_not_return_failed_for_stereo_issue_regressions(
    db_path: Path,
    stereo_issue_nonfailed_baseline_smiles: str,
) -> None:
    """Known stereo regressions should no longer fall back to failed scoring."""
    censor = ChemCensor(db_path=db_path)
    score = censor.score(stereo_issue_nonfailed_baseline_smiles)
    assert score != ScoringConfig.failed_reaction_scoring.value


def test_score_does_not_return_failed_for_sis_stereo_issue_regressions(
    db_path: Path,
    stereo_issue_nonfailed_sis_smiles: str,
) -> None:
    """Pure SIS regressions should not fall back to failed scoring."""
    censor = ChemCensor(db_path=db_path)
    score = censor.score(stereo_issue_nonfailed_sis_smiles)
    assert score != ScoringConfig.failed_reaction_scoring.value


def test_score_does_not_return_failed_for_pseudo_to_asymmetric_regressions(
    db_path: Path,
    stereo_issue_nonfailed_pseudo_to_asymmetric_smiles: str,
) -> None:
    """``r/s -> R/S`` regressions should not fall back to failed scoring."""
    censor = ChemCensor(db_path=db_path)
    score = censor.score(stereo_issue_nonfailed_pseudo_to_asymmetric_smiles)
    assert score != ScoringConfig.failed_reaction_scoring.value


def test_score_returns_failed_for_dynamic_q_to_rs_regression(
    db_path: Path,
    stereo_issue_failed_score_smiles: str,
) -> None:
    """Dynamic reactant ? -> product R/S remains inconsistent."""
    censor = ChemCensor(db_path=db_path)
    score = censor.score(stereo_issue_failed_score_smiles)
    assert score == ScoringConfig.failed_reaction_scoring.value


# ---------------------------------------------------------------------------
# Isomerization reaction scoring (inconsistent static centers → failed)
# ---------------------------------------------------------------------------

ISOMERIZATION_MAPPED_SMILES = (
    "[CH3:1][C:2](=[O:3])[C@@H:4]1[CH2:5][C@@H:6]2[CH2:7]"
    "[CH2:8][CH2:9][C@H:10]1[CH2:11][CH2:12]2>>[CH3:1]"
    "[C:2](=[O:3])[C@H:4]1[CH2:5][C@@H:6]2[CH2:7][CH2:8]"
    "[CH2:9][C@H:10]1[CH2:11][CH2:12]2"
)


def test_score_returns_failed_for_isomerization(db_path: Path) -> None:
    """Isomerization with inconsistent static centers → failed_reaction_scoring."""
    smiles = _strip_atom_maps(ISOMERIZATION_MAPPED_SMILES)
    censor = ChemCensor(db_path=db_path)
    score = censor.score(smiles)
    assert score == ScoringConfig.failed_reaction_scoring.value


LOST_STEREO_SMILES = (
    "C1CCOC1.CC(C)(C)O.CC(C)(C)[O-].CO."
    "COC(=O)C(c1c[nH]c2ccccc12)C(C(=O)OC)c1cn2c3c(cccc13)CCC2.N."
    "NCc1ccccc1."
    "O=C1NC(=O)[C@@H](c2cn3c4c(cccc24)CCC3)[C@@H]1c1c[nH]c2ccccc12."
    "O=C1[C@@H](c2c[nH]c3ccccc23)[C@H](c2cn3c4c(cccc24)CCC3)C(=O)N1c1ccccc1."
    "[K+].[Pd]>>"
    "O=C1NC(=O)C(c2cn3c4c(cccc24)CCC3)C1c1c[nH]c2ccccc12"
)


MULTI_STEREO_SMILES = (
    "CC(=O)[C@H]1CC[C@H]2[C@@H]3CC[C@H]4C[C@H](N=[N+]=[N-])CC[C@]4(C)"
    "[C@H]3CC[C@]12C.CCO.ClC(Cl)Cl.ClCCl.c1cc[nH+]cc1>>"
    "C[C@]12CC[C@@H](N=[N+]=[N-])C[C@@H]1CC[C@@H]1[C@@H]2CC[C@]2(C)"
    "[C@@H](C(=O)CBr)CC[C@@H]12"
)


def test_score_multi_stereo_does_not_crash(db_path: Path) -> None:
    """Reaction with many stereo centers processes without RuntimeError."""
    censor = ChemCensor(db_path=db_path)
    score = censor.score(MULTI_STEREO_SMILES)
    assert score == ScoringConfig.default_reaction_scoring.value


def test_score_returns_failed_for_lost_stereo(db_path: Path) -> None:
    """Reactant stereo centers lost in product → failed_reaction_scoring."""
    censor = ChemCensor(db_path=db_path)
    score = censor.score(LOST_STEREO_SMILES)
    assert score == ScoringConfig.failed_reaction_scoring.value


# ---------------------------------------------------------------------------
# Tautomerization reaction scoring
# ---------------------------------------------------------------------------

TAUTOMERIZATION_SMILES = [
    "CC1=CC=NN1>>CC2=NNC=C2",
    "OC1=CC=CC=N1>>O=C2C=CC=CN2",
]


@pytest.mark.parametrize(
    "reaction_smiles",
    TAUTOMERIZATION_SMILES,
    ids=[s[:30] for s in TAUTOMERIZATION_SMILES],
)
def test_score_returns_tautomerization_scoring(
    reaction_smiles: str,
    db_path: Path,
) -> None:
    """Tautomerization reaction → tautomerization_reaction_scoring."""
    censor = ChemCensor(db_path=db_path)
    score = censor.score(reaction_smiles)
    assert score == ScoringConfig.tautomerization_reaction_scoring.value


# ---------------------------------------------------------------------------
# FG-signature validation in scoring
# ---------------------------------------------------------------------------


def _extract_centers(fixture_id: int, max_ct: int = 4) -> Reaction:
    """Run the full pipeline on a fixture to obtain reaction centers."""
    fixture = _get_fixture(fixture_id)
    smiles = _strip_atom_maps(fixture["mapped_reaction_smiles"])
    reaction = Reaction(reaction_smiles=smiles)
    reaction = ReactionProcessor().process(reaction)
    extractor = ReactionCenterExtractor(
        max_center_type=ReactionCenterType(max_ct),
    )
    return extractor.extract_rc(reaction)


@pytest.fixture(scope="module")
def fixture_1_reaction() -> Reaction:
    """Fixture 1 processed through the full pipeline with RC1–RC4."""
    return _extract_centers(fixture_id=1, max_ct=4)


def _build_manager(
    reaction: Reaction,
    fg_overrides: dict[ReactionCenterType, np.ndarray] | None = None,
) -> DBManager:
    """Build an in-memory DB with centers from *reaction*.

    Each center uses its extracted ``fg_signature`` unless overridden
    via *fg_overrides*. Bridge rows use the reaction's canonical SMILES and
    ``sear_signature`` so scoring can resolve
    :meth:`~chemcensor.db.manager.DBManager.has_center_sear_in_bridge`
    and aggregate FG references.
    """
    db = DBManager()
    sear_sig = np.asarray(reaction.sear_signature, dtype=np.uint8).reshape(-1)
    if sear_sig.size != FG_COLLECTION_SEAR.num_groups:
        sear_sig = np.zeros(FG_COLLECTION_SEAR.num_groups, dtype=np.uint8)

    for ct, rc in reaction.reaction_centers.items():
        fg = (
            fg_overrides[ct] if fg_overrides and ct in fg_overrides else rc.fg_signature
        )
        db.add_reaction_center(rc.reaction_center_smiles, fg)
        db.add_center_to_reaction(
            rc.reaction_center_smiles,
            reaction.canonical_smiles,
            fg,
            sear_sig,
        )
    return db


def test_score_fg_identical_signatures_pass(
    fixture_1_reaction: Reaction,
) -> None:
    """Centers in DB with identical FG signatures → all pass → max center score."""
    db = _build_manager(fixture_1_reaction)
    censor = ChemCensor(manager=db, find_exact_match=False)
    score = censor.score(fixture_1_reaction.reaction_smiles)
    max_ct = max(fixture_1_reaction.reaction_centers.keys())
    assert score == ScoringConfig[f"lc_{max_ct}_scoring"].value


def test_score_fg_ref_superset_passes(
    fixture_1_reaction: Reaction,
) -> None:
    """Reference FG is a superset of input (extra bits set) → all pass."""
    all_ones = np.ones(FG_SIGNATURE_LENGTH, dtype=np.uint8)
    overrides = {ct: all_ones for ct in fixture_1_reaction.reaction_centers}
    db = _build_manager(fixture_1_reaction, overrides)
    censor = ChemCensor(manager=db, find_exact_match=False)
    score = censor.score(fixture_1_reaction.reaction_smiles)
    max_ct = max(fixture_1_reaction.reaction_centers.keys())
    assert score == ScoringConfig[f"lc_{max_ct}_scoring"].value


def test_score_fg_mismatch_breaks_at_first_nonzero(
    fixture_1_reaction: Reaction,
) -> None:
    """All centers in DB with all-zeros ref FG → breaks at first center
    whose input FG has non-zero bits."""
    zeros = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
    overrides = {ct: zeros for ct in fixture_1_reaction.reaction_centers}
    db = _build_manager(fixture_1_reaction, overrides)
    censor = ChemCensor(manager=db, find_exact_match=False)
    score = censor.score(fixture_1_reaction.reaction_smiles)

    sorted_cts = sorted(fixture_1_reaction.reaction_centers.keys())
    first_nonzero_ct = next(
        (
            ct
            for ct in sorted_cts
            if np.any(fixture_1_reaction.reaction_centers[ct].fg_signature)
        ),
        None,
    )
    if first_nonzero_ct is None:
        pytest.skip("All centers have all-zero FG signatures in this fixture")

    if first_nonzero_ct == sorted_cts[0]:
        expected = ScoringConfig.default_reaction_scoring.value
    else:
        prev_ct = sorted_cts[sorted_cts.index(first_nonzero_ct) - 1]
        expected = ScoringConfig[f"lc_{prev_ct}_scoring"].value

    assert score == expected


# ---------------------------------------------------------------------------
# SEAr: shared RC1 in ``reaction_centers`` but missing bridge ``sear_signature``
# ---------------------------------------------------------------------------

# Unmapped reaction SMILES (mapped variants in the scenario description are
# equivalent inputs after the mapper / canonicalization pipeline).
SEAR_REF_TOLUENE_BROMINATION = "Cc1ccccc1>>Cc1c(Br)cccc1"
SEAR_REF_ACETYL_CHLORO_BROMINATION = "CC(=O)c1cccc(Cl)c1>>CC(=O)c1c(Br)ccc(Cl)c1"
SEAR_QUERY_ACETOPHENONE_BROMINATION = "CC(=O)c1ccccc1>>CC(=O)c1c(Br)cccc1"


def _process_extract_for_sear_db(
    reaction_smiles: str,
    *,
    max_center_type: ReactionCenterType = ReactionCenterType.RC1,
) -> Reaction:
    reaction = Reaction(reaction_smiles=reaction_smiles)
    reaction = ReactionProcessor().process(reaction)
    extractor = ReactionCenterExtractor(max_center_type=max_center_type)
    return extractor.extract_rc(reaction)


def _db_from_processed_reference_reactions(reactions: list[Reaction]) -> DBManager:
    """Populate centers, bridge rows, and reactions like
    :class:`ReactionCenterDBComposer`.
    """
    db = DBManager()
    for reaction in reactions:
        for rc in reaction.reaction_centers.values():
            existing = db.find_center(rc.reaction_center_smiles)
            if existing is not None:
                combined = np.bitwise_or(existing, rc.fg_signature)
                db.update(rc.reaction_center_smiles, combined)
            else:
                db.add_reaction_center(
                    rc.reaction_center_smiles,
                    rc.fg_signature,
                    is_multi_component=rc.is_reaction_center_composite,
                    components=list(rc.reaction_center_components),
                )
            if not db.find_center_to_reaction(
                rc.reaction_center_smiles,
                reaction.canonical_smiles,
            ):
                db.add_center_to_reaction(
                    rc.reaction_center_smiles,
                    reaction.canonical_smiles,
                    rc.fg_signature,
                    reaction.sear_signature,
                )
        if db.find_reaction(reaction.canonical_smiles) is None:
            db.add_reaction(reaction.canonical_smiles, "")
    return db


def test_sear_signature_functionality() -> None:
    """SEAr query shares RC1 with reference data but not ``sear_signature``.

    Reference examples (toluene and acetyl–chloro bromination) both yield the same
    RC1 string ``ccc>>cc(c)Br`` and distinct ``sear_signature`` values in the
    bridge table. Acetophenone bromination reuses that RC1 pattern but its
    ``sear_signature`` does not match any bridge row, so the center must be
    treated as *not found* for scoring even though ``reaction_centers`` contains
    the SMILES key.
    """
    ref_toluene = _process_extract_for_sear_db(SEAR_REF_TOLUENE_BROMINATION)
    ref_acetyl_cl = _process_extract_for_sear_db(SEAR_REF_ACETYL_CHLORO_BROMINATION)
    query = _process_extract_for_sear_db(SEAR_QUERY_ACETOPHENONE_BROMINATION)

    assert ref_toluene.is_sear_reaction
    assert ref_acetyl_cl.is_sear_reaction
    assert query.is_sear_reaction

    rc1_key = "ccc>>cc(c)Br"
    assert ref_toluene.reaction_centers[
        ReactionCenterType.RC1
    ].reaction_center_smiles == (rc1_key)
    assert ref_acetyl_cl.reaction_centers[
        ReactionCenterType.RC1
    ].reaction_center_smiles == (rc1_key)
    assert query.reaction_centers[ReactionCenterType.RC1].reaction_center_smiles == (
        rc1_key
    )

    assert not np.array_equal(query.sear_signature, ref_toluene.sear_signature)
    assert not np.array_equal(query.sear_signature, ref_acetyl_cl.sear_signature)

    db = _db_from_processed_reference_reactions([ref_toluene, ref_acetyl_cl])
    assert db.find_center(rc1_key) is not None
    assert not db.has_center_sear_in_bridge(rc1_key, query.sear_signature)

    censor = ChemCensor(
        manager=db,
        max_center_type=ReactionCenterType.RC1,
        find_exact_match=False,
    )
    score = censor.score(SEAR_QUERY_ACETOPHENONE_BROMINATION)
    assert score == ScoringConfig.default_reaction_scoring.value


def test_score_fg_mismatch_at_higher_center_returns_lower_score(
    fixture_1_reaction: Reaction,
) -> None:
    """RC1 with matching FG in DB, higher centers with all-zeros FG → if the
    next center's input has non-zero FG bits the loop breaks at lc_1."""
    sorted_cts = sorted(fixture_1_reaction.reaction_centers.keys())
    if len(sorted_cts) < 2:
        pytest.skip("Need at least two center types for this test")

    second_ct = sorted_cts[1]
    rc_second = fixture_1_reaction.reaction_centers[second_ct]
    if not np.any(rc_second.fg_signature):
        pytest.skip(f"RC{second_ct} has all-zero FG signature")

    zeros = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
    overrides = {ct: zeros for ct in sorted_cts[1:]}
    db = _build_manager(fixture_1_reaction, overrides)
    censor = ChemCensor(manager=db, find_exact_match=False)
    score = censor.score(fixture_1_reaction.reaction_smiles)
    assert score == ScoringConfig[f"lc_{sorted_cts[0]}_scoring"].value
