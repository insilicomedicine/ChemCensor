from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Sequence
from unittest.mock import patch

from rdkit import Chem

from chemcensor import ChemCensor
from chemcensor import ChemCensorConfig
from chemcensor import PrecedentStatus
from chemcensor import ReactionCenterType
from chemcensor import ScoringConfig
from chemcensor import TraceOutcome
from chemcensor.basic import Reaction
from chemcensor.processing.reaction_processor import build_processors
from chemcensor.processing.reaction_processor import ReactionProcessor
from chemcensor.rules.functional_groups import FUNCTIONAL_GROUPS


_THIS_DIR = Path(__file__).resolve().parent
_TESTS_DIR = _THIS_DIR.parent
_DB_PATH = _THIS_DIR / "fixtures" / "rc_db.db"
_REACTION_FIXTURES_PATH = (
    _TESTS_DIR / "unit" / "extraction" / "fixtures" / "reaction_centers_fixtures.json"
)


class _StubMapper:
    """Return one fixture mapping without loading rxnmapper."""

    def __init__(self, mapped_reaction_smiles: str) -> None:
        self._mapped_reaction_smiles = mapped_reaction_smiles
        self.batch_calls = 0

    def process(self, reaction: Reaction) -> Reaction:
        return replace(
            reaction,
            mapped_reaction_smiles=self._mapped_reaction_smiles,
        )

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        self.batch_calls += 1
        return tuple(self.process(reaction) for reaction in reactions)


def _fixture_mapping(fixture_id: int) -> str:
    fixtures = json.loads(_REACTION_FIXTURES_PATH.read_text(encoding="utf-8"))
    return next(
        fixture["mapped_reaction_smiles"]
        for fixture in fixtures
        if fixture["id"] == fixture_id
    )


def _strip_atom_maps(mapped_reaction_smiles: str) -> str:
    reactants, _, product = mapped_reaction_smiles.split(">")
    reactants_mol = Chem.MolFromSmiles(reactants)
    product_mol = Chem.MolFromSmiles(product)
    for atom in list(reactants_mol.GetAtoms()) + list(product_mol.GetAtoms()):
        atom.SetAtomMapNum(0)
    return f"{Chem.MolToSmiles(reactants_mol)}>>{Chem.MolToSmiles(product_mol)}"


def _stubbed_censor(
    mapped_reaction_smiles: str,
    *,
    find_exact_match: bool = False,
) -> ChemCensor:
    processors = list(build_processors(include_mapper=False))
    processors.insert(1, _StubMapper(mapped_reaction_smiles))
    return ChemCensor.open(
        _DB_PATH,
        config=ChemCensorConfig(find_exact_match=find_exact_match),
        processor=ReactionProcessor(tuple(processors)),
    )


def test_trace_matches_evaluate_and_explains_center_chain_failure() -> None:
    mapped = _fixture_mapping(3)
    reaction_smiles = _strip_atom_maps(mapped)
    censor = _stubbed_censor(mapped)

    result = censor.evaluate(reaction_smiles)
    trace = censor.trace(reaction_smiles)

    assert trace.result == result
    assert trace.outcome is TraceOutcome.CENTER_COVERAGE
    assert trace.chain_failed_at is ReactionCenterType.RC4
    assert trace.center_chain_failed_at is ReactionCenterType.RC4
    assert [center.center_type for center in trace.centers] == [
        ReactionCenterType.RC1,
        ReactionCenterType.RC2,
        ReactionCenterType.RC4,
    ]

    rc1, rc2, rc4 = trace.centers
    assert rc1.precedent_status is PrecedentStatus.REAL
    assert rc2.precedent_status is PrecedentStatus.REAL
    assert rc1.precedent_count > 0
    assert rc2.precedent_count > 0
    assert rc1.included_with_functional_groups
    assert rc2.included_with_functional_groups
    assert rc1.real_precedents
    assert all(not example.is_virtual for example in rc1.real_precedents)
    assert all(example.is_virtual for example in rc1.virtual_precedents)
    assert all(
        len(center.real_precedents) <= 3 and len(center.virtual_precedents) <= 3
        for center in trace.centers
    )
    assert all(
        example.reaction_smiles
        and isinstance(example.document_id, str)
        and isinstance(example.source, str)
        for center in trace.centers
        for example in center.real_precedents + center.virtual_precedents
    )
    assert {evidence.ui_name for evidence in rc1.functional_group_evidence} == set(
        rc1.required_functional_groups
    )
    assert all(
        evidence.name and evidence.ui_name and evidence.smarts
        for evidence in rc1.functional_group_evidence
    )
    assert all(
        evidence.real_precedents or evidence.virtual_precedents
        for evidence in rc1.functional_group_evidence
    )
    assert all(
        len(evidence.real_precedents) <= 3 and len(evidence.virtual_precedents) <= 3
        for center in trace.centers
        for evidence in center.functional_group_evidence
    )
    assert all(
        not example.is_virtual
        for evidence in rc1.functional_group_evidence
        for example in evidence.real_precedents
    )
    assert all(
        example.is_virtual
        for evidence in rc1.functional_group_evidence
        for example in evidence.virtual_precedents
    )

    assert rc4.precedent_status is PrecedentStatus.ABSENT
    assert rc4.precedent_count == 0
    assert not rc4.included_without_functional_groups
    assert not rc4.included_with_functional_groups
    assert rc4.missing_functional_groups == rc4.required_functional_groups
    assert rc4.real_precedents == ()
    assert rc4.virtual_precedents == ()
    assert all(
        evidence.real_precedents == () and evidence.virtual_precedents == ()
        for evidence in rc4.functional_group_evidence
    )


def test_trace_uses_human_readable_functional_group_names() -> None:
    mapped = _fixture_mapping(3)
    trace = _stubbed_censor(mapped).trace(_strip_atom_maps(mapped))
    known_ui_names = {str(group["ui_name"]) for group in FUNCTIONAL_GROUPS}
    required_names = {
        name for center in trace.centers for name in center.required_functional_groups
    }

    assert required_names
    assert required_names <= known_ui_names
    assert "CH-acid #12" in required_names


def test_trace_reports_exact_match_with_center_precedents() -> None:
    mapped = _fixture_mapping(3)
    raw = _strip_atom_maps(mapped)
    censor = _stubbed_censor(mapped, find_exact_match=True)
    with patch.object(
        censor._manager,
        "find_reaction_precedents",
        side_effect=lambda _smiles, *, is_virtual, limit: (
            [] if is_virtual else [(raw, "US-1234567-A1", "USPTO", False)]
        ),
    ):
        trace = censor.trace(raw)

    assert trace.outcome is TraceOutcome.EXACT_MATCH
    assert (
        trace.result.with_functional_groups == ScoringConfig.exact_match_scoring.value
    )
    assert trace.centers
    assert trace.exact_real_precedents
    assert trace.exact_real_precedents[0].document_id == "US-1234567-A1"
    assert trace.centers[0].real_precedents
    assert trace.centers[0].functional_group_evidence


def test_evaluate_does_not_load_precedent_examples() -> None:
    mapped = _fixture_mapping(3)
    censor = _stubbed_censor(mapped)

    with (
        patch.object(
            censor._manager,
            "find_center_precedents",
            side_effect=AssertionError("evaluate loaded center evidence"),
        ),
        patch.object(
            censor._manager,
            "find_center_fg_precedents",
            side_effect=AssertionError("evaluate loaded FG evidence"),
        ),
        patch.object(
            censor._manager,
            "count_center",
            side_effect=AssertionError("evaluate counted precedents"),
        ),
        patch(
            "chemcensor.chemcensor._functional_group_names",
            side_effect=AssertionError("evaluate built trace FG names"),
        ),
    ):
        result = censor.evaluate(_strip_atom_maps(mapped))

    assert result.with_functional_groups == 2.0


def test_exact_evaluate_does_not_load_document_evidence() -> None:
    mapped = _fixture_mapping(3)
    censor = _stubbed_censor(mapped, find_exact_match=True)

    with patch.object(
        censor._manager,
        "find_reaction_precedents",
        side_effect=AssertionError("evaluate loaded exact-match evidence"),
    ):
        result = censor.evaluate(_strip_atom_maps(mapped))

    assert result.with_functional_groups == ScoringConfig.exact_match_scoring.value


def test_trace_batch_maps_once_and_returns_evidence_in_order() -> None:
    mapped = _fixture_mapping(3)
    mapper = _StubMapper(mapped)
    processors = list(build_processors(include_mapper=False))
    processors.insert(1, mapper)
    censor = ChemCensor.open(
        _DB_PATH,
        config=ChemCensorConfig(find_exact_match=True),
        processor=ReactionProcessor(tuple(processors)),
    )
    raw = _strip_atom_maps(mapped)

    traces = censor.trace_batch([raw, raw])

    assert mapper.batch_calls == 1
    assert len(traces) == 2
    assert all(trace.outcome is TraceOutcome.EXACT_MATCH for trace in traces)
    assert all(trace.centers[0].real_precedents for trace in traces)
