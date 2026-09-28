from pathlib import Path
from unittest.mock import patch

import pytest

from chemcensor.basic import Reaction
from chemcensor.chemcensor import ChemCensor
from chemcensor.chemcensor import ScoreResult
from chemcensor.configs.scoring_configs import ScoringConfig
from chemcensor.db.manager import DBManager
from chemcensor.processing.reaction_processor import ReactionProcessor


def test_open_defaults_to_file_backed_readonly_database(tmp_path: Path) -> None:
    reaction_smiles = "CCO>>CC=O"
    source = DBManager()
    source.add_reaction(reaction_smiles, document_id="doc-1")
    db_path = tmp_path / "reference.sqlite"
    source.dump(db_path)

    opened_managers: list[DBManager] = []
    open_readonly = DBManager.open_readonly

    def capture_readonly_manager(path: str | Path) -> DBManager:
        manager = open_readonly(path)
        opened_managers.append(manager)
        return manager

    with (
        patch.object(
            DBManager,
            "open_readonly",
            side_effect=capture_readonly_manager,
        ) as readonly_mock,
        patch.object(
            DBManager,
            "load",
            side_effect=AssertionError("database was copied into memory"),
        ),
    ):
        censor = ChemCensor.open(
            db_path,
            processor=ReactionProcessor(processors=()),
        )

    readonly_mock.assert_called_once_with(db_path)
    reaction = Reaction(
        reaction_smiles=reaction_smiles,
        canonical_smiles=reaction_smiles,
    )
    assert censor.evaluate_processed(reaction) == ScoreResult.uniform(
        ScoringConfig.exact_match_scoring.value
    )

    with pytest.raises(RuntimeError, match="read-only"):
        opened_managers[0].add_reaction("CCN>>CC=N")


def test_open_downloads_default_database_when_path_is_omitted(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "default.sqlite"
    DBManager().dump(db_path)

    with patch(
        "chemcensor.chemcensor.resolve_database_path",
        return_value=db_path,
    ) as resolve:
        censor = ChemCensor.open(
            processor=ReactionProcessor(processors=()),
        )

    resolve.assert_called_once_with(None)
    assert censor._manager._readonly is True


def test_constructor_downloads_default_database_when_source_is_omitted(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "default.sqlite"
    DBManager().dump(db_path)

    with patch(
        "chemcensor.chemcensor.resolve_database_path",
        return_value=db_path,
    ) as resolve:
        censor = ChemCensor(processor=ReactionProcessor(processors=()))

    resolve.assert_called_once_with(None)
    assert censor._manager._readonly is True


def test_readonly_database_uri_escapes_special_path_characters(
    tmp_path: Path,
) -> None:
    reaction_smiles = "CCO>>CC=O"
    source = DBManager()
    source.add_reaction(reaction_smiles, document_id="doc-1")
    source.write_metadata({"db_version": "U3-1"})
    db_path = tmp_path / "reference ?# ü.sqlite"
    source.dump(db_path)

    readonly = DBManager.open_readonly(db_path)

    assert readonly.find_reaction(reaction_smiles) == ["doc-1"]
    assert DBManager.read_metadata(db_path) == {"db_version": "U3-1"}


def test_open_can_explicitly_load_writable_in_memory_copy(tmp_path: Path) -> None:
    source = DBManager()
    db_path = tmp_path / "reference.sqlite"
    source.dump(db_path)

    loaded_managers: list[DBManager] = []
    load = DBManager.load

    def capture_loaded_manager(path: str | Path) -> DBManager:
        manager = load(path)
        loaded_managers.append(manager)
        return manager

    with (
        patch.object(
            DBManager,
            "load",
            side_effect=capture_loaded_manager,
        ) as load_mock,
        patch.object(
            DBManager,
            "open_readonly",
            side_effect=AssertionError("database was opened read-only"),
        ),
    ):
        ChemCensor.open(
            db_path,
            readonly=False,
            processor=ReactionProcessor(processors=()),
        )

    load_mock.assert_called_once_with(db_path)
    loaded_managers[0].add_reaction("CCO>>CC=O")
    assert loaded_managers[0].find_reaction("CCO>>CC=O") == [""]


def test_evaluate_processed_does_not_exact_match_raw_smiles() -> None:
    reaction_smiles = "CCO>>CC=O"
    manager = DBManager()
    manager.add_reaction(reaction_smiles, document_id="doc-1")
    censor = ChemCensor(
        manager=manager,
        processor=ReactionProcessor(processors=()),
    )

    result = censor.evaluate_processed(Reaction(reaction_smiles=reaction_smiles))

    assert result != ScoreResult.uniform(ScoringConfig.exact_match_scoring.value)
    assert result.failure_reason is not None
