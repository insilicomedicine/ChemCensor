from importlib.metadata import version
from importlib.resources import files

import chemcensor
from chemcensor import CenterTrace
from chemcensor import ChemCensor
from chemcensor import ChemCensorConfig
from chemcensor import FailureReason
from chemcensor import FailureStage
from chemcensor import FunctionalGroupEvidence
from chemcensor import PrecedentExample
from chemcensor import PrecedentStatus
from chemcensor import ReactionCenterType
from chemcensor import ScoreResult
from chemcensor import ScoreTrace
from chemcensor import ScoringConfig
from chemcensor import ScoringOutcome
from chemcensor import TraceOutcome


def test_supported_integration_types_are_exported_from_top_level() -> None:
    assert chemcensor.__version__ == version("chemcensor")
    assert "__version__" in chemcensor.__all__
    assert CenterTrace is chemcensor.CenterTrace
    assert ChemCensor is chemcensor.ChemCensor
    assert FailureReason is chemcensor.FailureReason
    assert FailureStage is chemcensor.FailureStage
    assert FunctionalGroupEvidence is chemcensor.FunctionalGroupEvidence
    assert PrecedentExample is chemcensor.PrecedentExample
    assert PrecedentStatus is chemcensor.PrecedentStatus
    assert ScoreResult is chemcensor.ScoreResult
    assert ScoreTrace is chemcensor.ScoreTrace
    assert ChemCensorConfig is chemcensor.ChemCensorConfig
    assert ScoringConfig is chemcensor.ScoringConfig
    assert ScoringOutcome is chemcensor.ScoringOutcome
    assert TraceOutcome is chemcensor.TraceOutcome
    assert ReactionCenterType is chemcensor.ReactionCenterType

    assert {
        "ChemCensor",
        "CenterTrace",
        "FailureReason",
        "FailureStage",
        "FunctionalGroupEvidence",
        "PrecedentExample",
        "PrecedentStatus",
        "ScoreResult",
        "ScoreTrace",
        "ChemCensorConfig",
        "ScoringConfig",
        "ScoringOutcome",
        "TraceOutcome",
        "ReactionCenterType",
    } <= set(chemcensor.__all__)


def test_internal_implementation_types_are_not_exported() -> None:
    assert "DBManager" not in chemcensor.__all__
    assert "ReactionProcessor" not in chemcensor.__all__
    assert not hasattr(chemcensor, "DBManager")
    assert not hasattr(chemcensor, "ReactionProcessor")


def test_package_declares_pep_561_typing_support() -> None:
    assert files("chemcensor").joinpath("py.typed").is_file()
