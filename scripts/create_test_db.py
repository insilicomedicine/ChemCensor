from __future__ import annotations

import json
from pathlib import Path
from typing import cast
from typing import Sequence

from rdkit import Chem

from chemcensor.basic import Reaction
from chemcensor.basic import ReactionCenterType
from chemcensor.db.manager import DBManager
from chemcensor.extraction import ReactionCenterExtractor
from chemcensor.processing.base import Processor
from chemcensor.processing.mapper import Mapper
from chemcensor.processing.orphan_remover import OrphanRemover
from chemcensor.processing.reaction_processor import DEFAULT_PROCESSORS
from chemcensor.processing.reaction_processor import ReactionProcessor
from chemcensor.processing.sear_annotator import SeArAnnotator
from chemcensor.processing.sis_annotator import SisAnnotator
from chemcensor.processing.transform_creator import TransformCreator
from chemcensor.rules.functional_groups import FG_COLLECTION_SEAR


# Paths relative to repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_JSON = (
    REPO_ROOT
    / "tests"
    / "unit"
    / "extraction"
    / "fixtures"
    / "reaction_centers_fixtures.json"
)
OUTPUT_DB_DIR = REPO_ROOT / "tests" / "unit" / "fixtures"
OUTPUT_DB_PATH = OUTPUT_DB_DIR / "rc_db.db"

# Which fixture IDs to include, and up to which center type
# to extract (1=RC1 only, 4=RC1..RC4).
# Format: (max_center_type, fixture_id, ...)
FIXTURE_GROUPS: list[tuple[int, ...]] = [
    (4, 1, 2, 5, 10),  # full extraction (RC1–RC4)
    (1, 17, 19),  # RC1 only
    (2, 3, 4),  # up to RC2
    (3, 11, 14),  # up to RC3
]

PROCESSORS: Sequence[Processor] = cast(
    Sequence[Processor],
    (
        Mapper(),
        OrphanRemover(),
        TransformCreator(),
        SisAnnotator(),
        SeArAnnotator(FG_COLLECTION_SEAR),
    ),
)


def strip_atom_maps(mapped_rxn_smiles: str) -> str:
    """Strip atom map numbers from a mapped reaction SMILES and canonicalize."""
    reactants_str, _, product_str = mapped_rxn_smiles.split(">")
    reactants_mol = Chem.MolFromSmiles(reactants_str)
    product_mol = Chem.MolFromSmiles(product_str)
    for atom in reactants_mol.GetAtoms():
        atom.SetAtomMapNum(0)
    for atom in product_mol.GetAtoms():
        atom.SetAtomMapNum(0)
    return f"{Chem.MolToSmiles(reactants_mol)}>>{Chem.MolToSmiles(product_mol)}"


def load_reaction_fixtures(path: Path) -> list[dict]:
    """Load reaction fixtures from JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_fixture_by_id(fixtures: list[dict], fixture_id: int) -> dict:
    """Return the fixture with the given id."""
    for f in fixtures:
        if f["id"] == fixture_id:
            return f
    raise KeyError(f"Fixture id={fixture_id} not found")


def process_and_extract(
    fixture: dict,
    max_center_type: int,
    processor: ReactionProcessor,
) -> Reaction:
    """Run process + extract_rc for one fixture;
    return reaction with reaction_centers."""
    extractor = ReactionCenterExtractor(
        max_center_type=ReactionCenterType(max_center_type),
    )
    reaction_smiles = strip_atom_maps(fixture["mapped_reaction_smiles"])
    reaction = Reaction(reaction_smiles=reaction_smiles)
    reaction = processor.process(reaction)
    return extractor.extract_rc(reaction)


def add_reaction_to_db(db: DBManager, reaction: Reaction) -> None:
    """Insert reaction centers and the canonical reaction SMILES into the DB."""
    for rc in reaction.reaction_centers.values():
        db.add_reaction_center(rc.reaction_center_smiles, rc.fg_signature)
        db.add_center_to_reaction(
            rc.reaction_center_smiles,
            reaction.canonical_smiles,
            rc.fg_signature,
            reaction.sear_signature,
        )
    if reaction.canonical_smiles:
        db.add_reaction(reaction.canonical_smiles)


def main() -> None:
    """Create the test reaction-centers database (rc_db.db).

    Reads reaction fixtures from tests, runs the full pipeline (process + extract),
    and writes all reaction centers with their FG signatures into a SQLite file
    used by ChemCensor tests.

    Run from repo root (with project env activated, e.g. conda activate chemcensor):
    python scripts/create_test_db.py
    """

    fixtures = load_reaction_fixtures(FIXTURES_JSON)
    OUTPUT_DB_DIR.mkdir(parents=True, exist_ok=True)

    db = DBManager()
    processor = ReactionProcessor(processors=DEFAULT_PROCESSORS)

    for group in FIXTURE_GROUPS:
        max_center_type, *fixture_ids = group
        for fid in fixture_ids:
            fixture = get_fixture_by_id(fixtures, fid)
            reaction = process_and_extract(fixture, max_center_type, processor)
            add_reaction_to_db(db, reaction)

    db.dump(OUTPUT_DB_PATH)
    print(f"Created {OUTPUT_DB_PATH}")


if __name__ == "__main__":
    main()
