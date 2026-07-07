from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest
from rdkit import Chem

from chemcensor.basic import Reaction
from chemcensor.basic import ReactionCenterType
from chemcensor.chemcensor import ScoreResult
from chemcensor.configs.scoring_configs import ScoringConfig
from chemcensor.db.manager import DBManager
from chemcensor.extraction import ReactionCenterExtractor
from chemcensor.parallel import ParallelConfig
from chemcensor.parallel import score_batch
from chemcensor.parallel import score_file
from chemcensor.processing.reaction_processor import ReactionProcessor


_THIS_DIR = Path(__file__).resolve().parent
_TESTS_DIR = _THIS_DIR.parent
RC_DB_PATH = _THIS_DIR / "fixtures" / "rc_db.db"
REACTION_FIXTURES_PATH = (
    _TESTS_DIR / "unit" / "extraction" / "fixtures" / "reaction_centers_fixtures.json"
)

# These ids correspond to fixtures that ``scripts/create_test_db.py``
# inserted into ``rc_db.db`` — see ``FIXTURE_GROUPS`` there.
EXACT_MATCH_FIXTURE_IDS = (1, 2, 5, 10)


with open(REACTION_FIXTURES_PATH, "r", encoding="utf-8") as _f:
    _FIXTURES = json.load(_f)


def _get_fixture(fixture_id: int) -> dict:
    return next(f for f in _FIXTURES if f["id"] == fixture_id)


def _strip_atom_maps(mapped_rxn_smiles: str) -> str:
    """Strip atom maps and canonicalize — mirrors the integration helper."""
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
    if not RC_DB_PATH.exists():
        pytest.skip(
            f"rc_db.db not found at {RC_DB_PATH}; run scripts/create_test_db.py"
        )
    return RC_DB_PATH


@pytest.fixture(scope="module")
def small_config() -> ParallelConfig:
    """A tiny, deterministic configuration for the integration tests.

    Two workers and one mapper thread are enough to exercise the
    queue / sentinel / shutdown logic without burning CPU.
    """
    return ParallelConfig(
        n_workers=2,
        mapper_threads=1,
        batch_size=2,
        mapper_internal_batch_size=2,
        progress=False,
        checkpoint_interval=0,
    )


@pytest.mark.heavy_test
def test_score_batch_returns_exact_match_for_in_db_fixtures(
    db_path: Path, small_config: ParallelConfig
) -> None:
    """Reactions whose canonical SMILES are in the DB → exact_match_scoring."""
    smiles_list = [
        _strip_atom_maps(_get_fixture(fid)["mapped_reaction_smiles"])
        for fid in EXACT_MATCH_FIXTURE_IDS
    ]
    scores = score_batch(smiles_list, db_path=db_path, config=small_config)
    expected = ScoreResult.uniform(ScoringConfig.exact_match_scoring.value)
    assert scores == [expected] * len(smiles_list)


@pytest.mark.heavy_test
def test_score_batch_returns_failed_for_garbage(
    db_path: Path, small_config: ParallelConfig
) -> None:
    """Malformed SMILES short-circuit to failed_reaction_scoring."""
    scores = score_batch(
        [">>", "not-a-reaction"],
        db_path=db_path,
        config=small_config,
    )
    failed = ScoreResult.uniform(ScoringConfig.failed_reaction_scoring.value)
    assert scores == [failed] * 2


@pytest.mark.heavy_test
def test_score_batch_preserves_input_order(
    db_path: Path, small_config: ParallelConfig
) -> None:
    """Mixed valid + invalid input keeps positions aligned in the output."""
    valid = _strip_atom_maps(_get_fixture(1)["mapped_reaction_smiles"])
    inputs = [">>", valid, "not-a-reaction", valid]
    scores = score_batch(inputs, db_path=db_path, config=small_config)
    failed = ScoreResult.uniform(ScoringConfig.failed_reaction_scoring.value)
    exact = ScoreResult.uniform(ScoringConfig.exact_match_scoring.value)
    assert scores == [failed, exact, failed, exact]


@pytest.mark.heavy_test
def test_score_batch_return_dict(db_path: Path, small_config: ParallelConfig) -> None:
    """``return_dict=True`` produces a mapping keyed by input index."""
    valid = _strip_atom_maps(_get_fixture(1)["mapped_reaction_smiles"])
    scores = score_batch(
        [valid, ">>"], db_path=db_path, config=small_config, return_dict=True
    )
    assert scores == {
        0: ScoreResult.uniform(ScoringConfig.exact_match_scoring.value),
        1: ScoreResult.uniform(ScoringConfig.failed_reaction_scoring.value),
    }


@pytest.mark.heavy_test
def test_score_file_writes_results(
    tmp_path: Path, db_path: Path, small_config: ParallelConfig
) -> None:
    """``score_file`` writes one row per input with both score columns."""
    valid = _strip_atom_maps(_get_fixture(1)["mapped_reaction_smiles"])
    input_csv = tmp_path / "in.csv"
    output_csv = tmp_path / "out.csv"

    with open(input_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["reaction_smiles"])
        for smi in (valid, ">>", valid):
            w.writerow([smi])

    score_file(
        input_path=input_csv,
        output_path=output_csv,
        db_path=db_path,
        config=small_config,
    )

    with open(output_csv, encoding="utf-8") as fh:
        rows = list(csv.reader(fh))

    assert rows[0] == ["idx", "smiles", "score_with_fg", "score_without_fg"]
    failed = ScoringConfig.failed_reaction_scoring.value
    exact = ScoringConfig.exact_match_scoring.value

    # Both score columns carry the same value for exact-match / failed rows.
    seen = {int(r[0]): (float(r[2]), float(r[3])) for r in rows[1:]}
    # All three input rows reach the worker — ">>" is a non-empty SMILES
    # so the reader keeps it; the worker resolves it to ``failed``.
    assert set(seen) == {0, 1, 2}
    assert seen[0] == (exact, exact)
    assert seen[1] == (failed, failed)
    assert seen[2] == (exact, exact)


@pytest.mark.heavy_test
def test_resume_does_not_duplicate_out_of_order_rows(
    tmp_path: Path, db_path: Path
) -> None:
    """Resume skips already-written out-of-order rows (no duplicate idx).

    Regression test: the checkpoint persists only ``last_contiguous_idx``
    plus the out-of-order ``completed_above`` set. Without the latter, rows
    with ``idx > last_contiguous_idx`` that were already flushed during the
    first run get re-scored and re-appended on resume → duplicate ``idx``
    in the output CSV.

    We simulate an interrupted first run: idx 0,1,2 are contiguous and 4,5
    finished out of order (3 and 6 are still missing). On resume only 3 and
    6 must be scored, and every idx must appear exactly once.
    """
    from chemcensor.parallel import checkpoint as ckpt_mod

    mapped = [
        _get_fixture(fid)["mapped_reaction_smiles"] for fid in EXACT_MATCH_FIXTURE_IDS
    ]
    # 7 input rows of precomputed atom-mapped reactions.
    inputs = [mapped[i % len(mapped)] for i in range(7)]

    input_csv = tmp_path / "in.csv"
    output_csv = tmp_path / "out.csv"
    ckpt = tmp_path / "state.ckpt"

    with open(input_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["reaction_smiles"])
        for smi in inputs:
            w.writerow([smi])

    # Simulate the first run's partial output: contiguous 0,1,2 and the
    # out-of-order 4,5 already written.
    already_done = [0, 1, 2, 4, 5]
    with open(output_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["idx", "smiles", "score_with_fg", "score_without_fg"])
        for i in already_done:
            w.writerow([i, inputs[i], 0.0, 0.0])

    ckpt_mod.save(
        ckpt,
        ckpt_mod.CheckpointState(
            last_contiguous_idx=2,
            completed_count=len(already_done),
            completed_above=frozenset({4, 5}),
        ),
    )

    config = ParallelConfig(
        n_workers=2,
        mapper_threads=1,
        batch_size=2,
        mapper_internal_batch_size=2,
        use_fake_mapper=True,
        progress=False,
        checkpoint_interval=0,
    )

    score_file(
        input_path=input_csv,
        output_path=output_csv,
        db_path=db_path,
        config=config,
        checkpoint_path=ckpt,
    )

    with open(output_csv, encoding="utf-8") as fh:
        rows = list(csv.reader(fh))

    assert rows[0] == ["idx", "smiles", "score_with_fg", "score_without_fg"]
    written = [int(r[0]) for r in rows[1:]]
    # Every input scored exactly once — no duplicates from re-feeding 4/5.
    assert sorted(written) == list(range(7))
    assert len(written) == len(set(written))

    # Checkpoint frontier advanced cleanly to the end.
    final = ckpt_mod.load(ckpt)
    assert final.last_contiguous_idx == 6
    assert final.completed_above == frozenset()


@pytest.mark.heavy_test
def test_maxtasksperchild_recycle_scores_all_inputs(db_path: Path) -> None:
    """Recycled scorers are respawned, so no input is silently dropped.

    Regression test for the data-loss bug: when
    ``maxtasksperchild * n_workers < number of batches`` every worker used
    to exit (emitting a terminal sentinel) before the queue was drained, so
    the writer counted all workers done, reported success, and left the
    tail unscored. The orchestrator now respawns a recycled worker into the
    same slot, so the whole input is scored.

    Uses the fake-mapper path so the test needs neither rxnmapper nor a GPU;
    the fixtures' precomputed atom maps are fed straight in.
    """
    mapped = [
        _get_fixture(fid)["mapped_reaction_smiles"] for fid in EXACT_MATCH_FIXTURE_IDS
    ]
    # 8 single-reaction batches with maxtasksperchild=3 and 2 workers means
    # the first generation (6 batches) recycles before the tail is reached —
    # exactly the condition that used to drop reactions.
    inputs = mapped * 2  # 8 reactions
    config = ParallelConfig(
        n_workers=2,
        mapper_threads=1,
        batch_size=1,
        mapper_internal_batch_size=1,
        maxtasksperchild=3,
        use_fake_mapper=True,
        progress=False,
        checkpoint_interval=0,
    )

    scores = score_batch(inputs, db_path=db_path, config=config, return_dict=True)

    exact = ScoreResult.uniform(ScoringConfig.exact_match_scoring.value)
    assert set(scores) == set(range(len(inputs)))
    assert all(scores[i] == exact for i in range(len(inputs)))


@pytest.mark.heavy_test
def test_score_file_resume_from_checkpoint(
    tmp_path: Path, db_path: Path, small_config: ParallelConfig
) -> None:
    """Re-running with the same ``.ckpt`` skips already-completed rows."""
    valid = _strip_atom_maps(_get_fixture(1)["mapped_reaction_smiles"])
    input_csv = tmp_path / "in.csv"
    output_csv = tmp_path / "out.csv"
    ckpt = tmp_path / "state.ckpt"

    with open(input_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["reaction_smiles"])
        for _ in range(4):
            w.writerow([valid])

    # First pass: score everything, write a checkpoint.
    score_file(
        input_path=input_csv,
        output_path=output_csv,
        db_path=db_path,
        config=small_config,
        checkpoint_path=ckpt,
    )

    with open(output_csv, encoding="utf-8") as fh:
        first_run = list(csv.reader(fh))[1:]
    assert len(first_run) == 4

    # Second pass: checkpoint indicates everything is done → no new rows.
    score_file(
        input_path=input_csv,
        output_path=output_csv,
        db_path=db_path,
        config=small_config,
        checkpoint_path=ckpt,
    )
    with open(output_csv, encoding="utf-8") as fh:
        second_run = list(csv.reader(fh))[1:]
    assert second_run == first_run


# Fixture 19 with an extra nitro group on the remote ester arm: the RC1 center
# is unchanged (so it matches a DB entry built from the original fixture), but
# the added functional group makes the RC1 FG sub-signature no longer a subset
# of the stored reference. Mirrors the constant in ``test_chemcensor.py``.
FIXTURE_19_WITH_EXTRA_FG_RXN_SMILES = (
    "CC([N+]([O-])=O)OC([C@@H]1CCNC[C@@H]1OC2CCCCO2)=O."
    "FC(F)(c(cc3n4nccc4)nc5c3cc(Cl)cc5)F>>"
    "CC([N+]([O-])=O)OC([C@@H]6CCN(C[C@@H]6OC7CCCCO7)c(cc8)cc9c8nc(C(F)(F)F)"
    "cc9n%10nccc%10)=O"
)


@pytest.mark.heavy_test
def test_score_batch_distinguishes_fg_variants(tmp_path: Path) -> None:
    """``score_batch`` reports both FG variants per reaction in one pass.

    The DB holds fixture 19's genuine RC1 center and FG signature; the scored
    reaction adds an extra functional group, so the center is found but its FG
    sub-signature no longer matches. The single returned ``ScoreResult`` must
    carry ``default`` with the FG check and ``lc_1`` without it.
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
    db_file = tmp_path / "rc19.db"
    db.dump(db_file)

    config = ParallelConfig(
        n_workers=1,
        mapper_threads=1,
        batch_size=1,
        mapper_internal_batch_size=1,
        max_center_type=1,
        find_exact_match=False,
        progress=False,
        checkpoint_interval=0,
    )

    scores = score_batch(
        [FIXTURE_19_WITH_EXTRA_FG_RXN_SMILES], db_path=db_file, config=config
    )

    assert scores == [
        ScoreResult(
            with_functional_groups=ScoringConfig.default_reaction_scoring.value,
            without_functional_groups=ScoringConfig.lc_1_scoring.value,
        )
    ]
