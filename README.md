# ChemCensor

[![Dataset](https://img.shields.io/badge/Dataset-Hugging%20Face-FFD21F?style=flat-square&logo=huggingface&logoColor=black)](https://huggingface.co/datasets/insilicomedicine/chemcensor)
[![Paper](https://img.shields.io/badge/Paper-arXiv%3A2602.03554-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2602.03554)

ChemCensor is a precedent-based framework for evaluating reaction chemical plausibility.
It separates the **reaction center** (what changes) from the **functional-group context** (what must be tolerated), then checks whether similar patterns are supported by known precedents stored in an SQLite database.

The resulting **ChemCensor Score** is an integer confidence level from 0 to 5, where higher values indicate stronger precedent support.

---

## Installation

Requires Python ≥ 3.12.

```bash
python -m pip install -e .            # runtime dependencies
python -m pip install -e ".[dev]"     # + dev/test tooling
```

Dependencies are pinned in `requirements/requirements.txt` (runtime) and
`requirements/requirements-dev.txt` (development).

---

## Scoring scale

`score()` returns a single float; `evaluate()` returns both functional-group
variants. The possible values (`ScoringConfig`):

| Value  | Meaning                                              |
| ------ | --------------------------------------------------- |
| `5.0`  | Exact match — canonical reaction SMILES is in the DB |
| `4.0`  | Reaction center of type RC4 matched                  |
| `3.0`  | Reaction center of type RC3 matched                  |
| `2.0`  | Reaction center of type RC2 matched                  |
| `1.0`  | RC1 matched (also SIS / tautomerization reactions)   |
| `0.0`  | Default — no center matched                           |
| `-1.0` | Failed — reaction could not be processed             |

---

## Download DB and use with ChemCensor

Below is a complete step-by-step workflow with commands.

### 1) Clone and install ChemCensor

```bash
git clone https://github.com/insilicomedicine/ChemCensor.git
cd ChemCensor
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

### 2) Download the SQLite database archive

```bash
mkdir -p data
hf download insilicomedicine/chemcensor \
  --repo-type dataset \
  --include "ChemCensor-DB-U2-1.0.0.sqlite.zip" \
  --local-dir data
```

### 3) Unpack the database

```bash
unzip -j -o data/ChemCensor-DB-U2-1.0.0.sqlite.zip -d data/
```

After unpacking you should have:

```text
data/ChemCensor-DB-U2-1.0.0.sqlite
```

### 4) Use the database in Python

```python
from chemcensor import ChemCensor

db_path = "data/ChemCensor-DB-U2-1.0.0.sqlite"
censor = ChemCensor(db_path=db_path)

reaction_smiles = "CCO.CC(=O)O>>CCOC(=O)C"
score = censor.score(reaction_smiles)
print(score)
```

> `db_path` can point to any local `.sqlite` file location; using `data/` is a convenient project convention.

---

## Usage

The examples below use `data/ChemCensor-DB-U2-1.0.0.sqlite` from the workflow
above;

### Single reaction (in-process)

```python
from chemcensor import ChemCensor

censor = ChemCensor(db_path="data/ChemCensor-DB-U2-1.0.0.sqlite")
score = censor.score("CCO.CC(=O)O>>CCOC(=O)C")
```

Constructor options (keyword-only):

- `db_path` **or** `manager` — exactly one reaction-center DB source.
- `max_center_type` — highest reaction-center type to extract (1–4, default 4).
- `find_exact_match` — short-circuit to `5.0` on a canonical-SMILES hit
  (default `True`).
- `check_functional_groups` — require each center's functional-group
  sub-signature to match the DB reference (default `True`). Affects only
  `score()` / `score_processed()`.

### Both score variants in one pass

`evaluate()` runs the (expensive) pipeline once and returns a `ScoreResult`
with both the functional-group aware and agnostic scores:

```python
from chemcensor import ChemCensor, ScoreResult

censor = ChemCensor(db_path="data/ChemCensor-DB-U2-1.0.0.sqlite")
result: ScoreResult = censor.evaluate("CCO.CC(=O)O>>CCOC(=O)C")

result.with_functional_groups        # score requiring FG sub-signature match
result.without_functional_groups     # score on reaction-center presence only
result.select(check_functional_groups=False)  # pick one by flag
```

### Batch scoring in parallel (in-process)

```python
from chemcensor.parallel import score_batch, ParallelConfig

db_path = "data/ChemCensor-DB-U2-1.0.0.sqlite"

# list[ScoreResult], aligned with input order
results = score_batch(["CCO.CC(=O)O>>CCOC(=O)C", "A>>B"], db_path=db_path)
results[0].with_functional_groups

# or dict[int, ScoreResult] keyed by input position
as_dict = score_batch(smiles, db_path=db_path, return_dict=True)
```

### Scoring a CSV file

`score_file` streams results to an output CSV with the columns
`idx, smiles, score_with_fg, score_without_fg`. Rows are written as workers
complete them (not input order) — sort by `idx` if needed.

```python
from chemcensor.parallel import score_file, ParallelConfig

score_file(
    input_path="in.csv",
    output_path="out.csv",
    db_path="data/ChemCensor-DB-U2-1.0.0.sqlite",
    smiles_column="reaction_smiles",
    config=ParallelConfig(n_workers=8),  # None = autoscale to CPU count
    checkpoint_path="run.ckpt",          # optional, enables resume
)
```

Or from the command line:

```bash
python scripts/score_parallel.py in.csv out.csv --db data/ChemCensor-DB-U2-1.0.0.sqlite
```

Useful flags: `--workers N`, `--smiles-column NAME`, `--checkpoint run.ckpt`,
`--fake-mapper` (reuse precomputed atom maps instead of running rxnmapper),
`--no-exact-match`, `--max-center-type {1,2,3,4}`.

---

## Building the reaction-center database

Compose a database from a reference CSV of reactions:

```bash
python scripts/compose_database.py reactions.csv rc_db.db \
    --reaction-smiles-column cleaned_rxn \
    --document-id-column PatentNumber
```

---

## Development

```bash
python -m pip install -e ".[dev]"
pre-commit run --all-files     # lint / format / type checks
pytest                         # run the test suite
pytest -m "not heavy_test"     # skip the heavy parallel integration tests
```

---

## License

ChemCensor is released under a license for **independent benchmarking and evaluation purposes only**. Use in products, pipelines, automated workflows, or redistribution requires prior written permission from Insilico. See [LICENSE](LICENSE) for full terms.

---

## Citation

If you use ChemCensor in your work, please cite:

```bibtex
@misc{zagribelnyy2026singleanswerenoughrethinking,
      title={When Single Answer Is Not Enough: Rethinking Single-Step Retrosynthesis Benchmarks for LLMs},
      author={Bogdan Zagribelnyy and Ivan Ilin and Maksim Kuznetsov and Nikita Bondarev and Roman Schutski
                and Thomas MacDougall and Rim Shayakhmetov and Zulfat Miftakhutdinov
                and Mikolaj Mizera and Vladimir Aladinskiy and Alex Aliper and Alex Zhavoronkov},
      year={2026},
      eprint={2602.03554},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2602.03554}
}
```

and/or:

```bibtex
@misc{zagribelnyy2026ursachemistryawarebenchmarkutilitarian,
      title={URSA: Chemistry-Aware Benchmark for Utilitarian Retrosynthesis Assessment},
      author={Bogdan Zagribelnyy and Ivan Ilin and Nikita Bondarev and Anton Morgunov and Arkadii Lin and Maksim Kuznetsov and Rim Shayakhmetov and Vladimir Aladinskiy and Alex Aliper and Alex Zhavoronkov},
      year={2026},
      eprint={2607.04688},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2607.04688},
}
```
