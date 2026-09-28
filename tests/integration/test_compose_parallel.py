from __future__ import annotations

import csv
import shutil
from pathlib import Path

import numpy as np
import pytest

from chemcensor.parallel import compose_file
from chemcensor.parallel import ParallelConfig


_THIS_DIR = Path(__file__).resolve().parent
_TESTS_DIR = _THIS_DIR.parent
REFERENCE_CSV = _TESTS_DIR / "unit" / "composition" / "reaction_database_test.csv"


def _build_serial_db(csv_path: Path, output: Path) -> None:
    """Compose serially with the same pipeline the parallel worker uses."""
    from chemcensor.basic import ReactionCenterType
    from chemcensor.composition import ReactionCenterDBComposer
    from chemcensor.configs import CompositionPipelineConfig
    from chemcensor.extraction import ReactionCenterExtractor

    processor = CompositionPipelineConfig(mapper_batch_size=16).build_processor()
    extractor = ReactionCenterExtractor(max_center_type=ReactionCenterType.RC4)
    composer = ReactionCenterDBComposer(
        processor=processor,
        reaction_center_extractor=extractor,
        batch_size=16,
        reaction_smiles_column="reaction_smiles",
        document_id_column="document_id",
    )
    composer.compose(csv_path, output, db_version="U9-TEST")


def _dump_db(path: Path) -> dict:
    """Return a comparable snapshot of a composed database."""
    from chemcensor.db import DBManager

    db = DBManager.load(path)
    centers = {
        smiles: np.frombuffer(sig, dtype=np.uint8).tobytes()
        for smiles, sig in db._conn.execute(
            "SELECT reaction_center_smiles, fg_signature FROM reaction_centers"
        ).fetchall()
    }
    reactions = set(
        db._conn.execute(
            "SELECT reaction_smiles, document_id FROM reactions"
        ).fetchall()
    )
    bridge = set(
        db._conn.execute(
            "SELECT reaction_center_smiles, reaction_smiles FROM centers_to_reactions"
        ).fetchall()
    )
    return {"centers": centers, "reactions": reactions, "bridge": bridge}


@pytest.mark.heavy_test
def test_parallel_compose_matches_serial(tmp_path: Path) -> None:
    """A parallel build must yield the same database as the serial one.

    Requires RDKit and rxnmapper, so marked heavy.
    """
    if not REFERENCE_CSV.exists():
        pytest.skip(f"Reference CSV not found: {REFERENCE_CSV}")

    serial_db = tmp_path / "serial.sqlite"
    parallel_db = tmp_path / "parallel.sqlite"

    _build_serial_db(REFERENCE_CSV, serial_db)

    compose_file(
        db_version="U9-TEST",
        input_path=REFERENCE_CSV,
        output_path=parallel_db,
        reaction_smiles_column="reaction_smiles",
        document_id_column="document_id",
        config=ParallelConfig(
            n_workers=2,
            n_mappers=1,
            batch_size=16,
            progress=False,
        ),
    )

    serial = _dump_db(serial_db)
    parallel = _dump_db(parallel_db)

    assert set(parallel["centers"]) == set(serial["centers"])
    assert parallel["centers"] == serial["centers"]
    assert parallel["reactions"] == serial["reactions"]
    assert parallel["bridge"] == serial["bridge"]


@pytest.mark.heavy_test
def test_saved_atom_maps_let_a_rerun_skip_rxnmapper(tmp_path: Path) -> None:
    """``save_mapped_path`` makes the input CSV reusable with the fake mapper.

    The whole point of persisting the maps is that a second build over the same
    CSV must not need rxnmapper and must still produce the same database.
    """
    if not REFERENCE_CSV.exists():
        pytest.skip(f"Reference CSV not found: {REFERENCE_CSV}")

    reactions_csv = tmp_path / "reactions.csv"
    shutil.copy(REFERENCE_CSV, reactions_csv)
    mapped_db = tmp_path / "mapped.sqlite"
    reused_db = tmp_path / "reused.sqlite"
    config = ParallelConfig(n_workers=2, n_mappers=1, batch_size=16, progress=False)

    compose_file(
        db_version="U9-TEST",
        input_path=reactions_csv,
        output_path=mapped_db,
        reaction_smiles_column="reaction_smiles",
        document_id_column="document_id",
        config=config,
        save_mapped_path=reactions_csv,
    )

    with open(reactions_csv, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    # Original columns survive and the new one carries atom maps.
    assert rows[0]["reaction_smiles"] and rows[0]["document_id"]
    assert sum(1 for row in rows if row["mapped_rxn"]) > 0
    assert all(":1]" in row["mapped_rxn"] for row in rows if row["mapped_rxn"])
    assert not list(tmp_path.glob(".chemcensor-mapped-*"))

    compose_file(
        db_version="U9-TEST",
        input_path=reactions_csv,
        output_path=reused_db,
        reaction_smiles_column="mapped_rxn",
        document_id_column="document_id",
        config=ParallelConfig(
            n_workers=2,
            n_mappers=2,
            batch_size=1,
            maxtasksperchild=2,
            progress=False,
            use_fake_mapper=True,
        ),
    )

    assert _dump_db(reused_db) == _dump_db(mapped_db)


@pytest.mark.heavy_test
def test_parallel_compose_writes_build_stamp(tmp_path: Path) -> None:
    """A parallel build must stamp the database the same way a serial one does."""
    from chemcensor.db import DBManager

    if not REFERENCE_CSV.exists():
        pytest.skip(f"Reference CSV not found: {REFERENCE_CSV}")

    output = tmp_path / "parallel.sqlite"
    compose_file(
        db_version="U9-TEST",
        input_path=REFERENCE_CSV,
        output_path=output,
        reaction_smiles_column="reaction_smiles",
        document_id_column="document_id",
        config=ParallelConfig(n_workers=2, n_mappers=1, batch_size=16, progress=False),
    )

    metadata = DBManager.read_metadata(output)
    assert metadata["db_version"] == "U9-TEST"
    assert metadata["built_at"]
    assert metadata["chemcensor_version"]
