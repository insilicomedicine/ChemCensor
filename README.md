# ChemCensor

Library for scoring organic reactions against a database of reaction centers (extracted reaction contexts and functional-group signatures).
It maps and normalizes reactions, detects reaction centers, and compares them to a reference SQLite database.

## Requirements

- Python 3.12+
- Dependencies are listed in `requirements/requirements.txt` (RDKit, NumPy, RxnMapper, etc.).

## Install

From the repository root:

```bash
pip install -e .
```

## Development

```bash
pip install -e ".[dev]"
pre-commit install
pytest
```

Linting and static checks (also run in CI):

```bash
flake8 .
black . --check
mypy .
bandit -c pyproject.toml -r src/chemcensor
```

## Usage sketch

```python
from chemcensor import ChemCensor

censor = ChemCensor(db_path="path/to/reaction_centers.db")
score = censor.score("mapped_reaction_smiles>>product")
```

See tests under `tests/` and `scripts/create_test_db.py` for building a small reference database from fixtures.
