import csv
from pathlib import Path
from unittest.mock import patch

import pytest

from chemcensor.db.errors import InvalidDBVersionError
from chemcensor.parallel import compose_file


def _write_csv(path: Path) -> None:
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["cleaned_rxn", "document_id"])
        writer.writerow(["A>>B", "doc1"])


class TestComposeFileRequiresVersionLabel:
    def test_blank_label_fails_before_starting_workers(self, tmp_path: Path):
        csv_path = tmp_path / "in.csv"
        _write_csv(csv_path)

        with patch(
            "chemcensor.parallel.composition_orchestrator.run_composition"
        ) as mock_run:
            with pytest.raises(InvalidDBVersionError, match="db_version"):
                compose_file(
                    input_path=csv_path,
                    output_path=tmp_path / "out.sqlite",
                    reaction_smiles_column="cleaned_rxn",
                    db_version="",
                )

        mock_run.assert_not_called()

    def test_label_is_passed_through_to_the_orchestrator(self, tmp_path: Path):
        csv_path = tmp_path / "in.csv"
        _write_csv(csv_path)

        with patch(
            "chemcensor.parallel.composition_orchestrator.run_composition"
        ) as mock_run:
            compose_file(
                input_path=csv_path,
                output_path=tmp_path / "out.sqlite",
                reaction_smiles_column="cleaned_rxn",
                db_version="U9-TEST",
            )

        assert mock_run.call_args.kwargs["db_version"] == "U9-TEST"


class TestRunCompositionRequiresVersionLabel:
    def test_blank_label_fails_before_spawning_processes(self):
        from chemcensor.parallel import ParallelConfig
        from chemcensor.parallel.composition_orchestrator import run_composition

        # Raise instead of returning a mock: without the guard the pipeline
        # starts and this test would hang rather than fail.
        with patch(
            "chemcensor.parallel.composition_orchestrator.mp.get_context",
            side_effect=AssertionError("started the pipeline before validating"),
        ):
            with pytest.raises(InvalidDBVersionError, match="db_version"):
                run_composition(
                    source=iter([]),
                    output_path="unused.sqlite",
                    idx_to_doc={},
                    config=ParallelConfig(n_workers=1, n_mappers=1),
                    db_version="   ",
                )
