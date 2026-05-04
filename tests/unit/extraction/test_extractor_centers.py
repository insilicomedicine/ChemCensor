from __future__ import annotations

import json
from dataclasses import dataclass

import pytest

from chemcensor.basic import Reaction
from chemcensor.basic.reaction_center import ReactionCenterType
from chemcensor.basic.reaction_transform import ReactionTransform
from chemcensor.extraction.extractor import Extractor


@dataclass(frozen=True)
class RCFixture:
    """A single reaction center from the legacy benchmark."""

    center_type: int
    unmapped_smarts: str


@dataclass(frozen=True)
class ReactionFixture:
    """One reaction with its legacy-extracted centers."""

    id: int
    number_of_reaction_centers: int
    mapped_reaction_smiles: str
    reaction_centers_fix: tuple[RCFixture, ...]


LEGACY_RC_FILE = "tests/unit/extraction/fixtures/reaction_centers_fixtures.json"

with open(LEGACY_RC_FILE, "r", encoding="utf-8") as f:
    _raw_fixtures = json.load(f)

reaction_centers_fixtures: list[ReactionFixture] = []

for reaction in _raw_fixtures:
    id = reaction["id"]
    number_of_reaction_centers = reaction["number_of_reaction_centers"]
    mapped_reaction_smiles = reaction["mapped_reaction_smiles"]
    reaction_centers_fix = reaction["reaction_centers"]
    reaction_center_fix_tuple: tuple[RCFixture, ...] = ()
    for center_type, unmapped_smarts in reaction_centers_fix.items():
        reaction_center_fix_tuple += (RCFixture(center_type, unmapped_smarts),)

    reaction_centers_fixtures.append(
        ReactionFixture(
            id=id,
            number_of_reaction_centers=number_of_reaction_centers,
            mapped_reaction_smiles=mapped_reaction_smiles,
            reaction_centers_fix=reaction_center_fix_tuple,
        )
    )


def _run_extractor(fixture: ReactionFixture) -> Reaction:
    """Create Reaction, run Extractor, return result."""
    T = ReactionTransform.from_reaction_smiles(fixture.mapped_reaction_smiles)
    reaction = Reaction(
        reaction_smiles=fixture.mapped_reaction_smiles,
        reaction_transform=T,
    )
    return Extractor(max_center_type=ReactionCenterType.RC4).extract_rc(reaction)


def _extracted_centers(fixture: ReactionFixture) -> set[str]:
    """Return set of ``reaction_center_smiles`` from the extractor."""
    result = _run_extractor(fixture)
    return {rc.reaction_center_smiles for rc in result.reaction_centers.values()}


def _fixture_centers(fixture: ReactionFixture) -> set[str]:
    """Return set of legacy ``reaction_center_smiles``."""
    return {lc.unmapped_smarts for lc in fixture.reaction_centers_fix}


@pytest.mark.parametrize(
    "fixture",
    reaction_centers_fixtures,
    ids=[f.id for f in reaction_centers_fixtures],
)
def test_reaction_center_extraction(fixture: ReactionFixture) -> None:
    """Test the legacy compatibility of the extractor."""
    extracted_centers = _extracted_centers(fixture)
    reaction_centers_fix = _fixture_centers(fixture)
    assert extracted_centers == reaction_centers_fix, (
        f"[{fixture.id}] centers mismatch.\n"
        f"  only in extracted: {sorted(extracted_centers - reaction_centers_fix)}\n"
        f"  only in legacy:    {sorted(reaction_centers_fix - extracted_centers)}"
    )
