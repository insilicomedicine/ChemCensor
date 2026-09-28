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

The runtime constraint `setuptools<81` is temporary: rxnmapper 0.4.2 imports
`pkg_resources`, which setuptools 81 removed.

The installed package exposes its distribution version as
`chemcensor.__version__` and ships a PEP 561 `py.typed` marker.

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

Clients can resolve the scale without hard-coding enum names or numeric values:

```python
from chemcensor import ReactionCenterType, ScoringConfig, ScoringOutcome

ScoringConfig.center_type_scoring(ReactionCenterType.RC4)  # 4.0
ScoringConfig.outcome_scoring(ScoringOutcome.FAILED)        # -1.0
ScoringConfig.outcome_meaning(ScoringOutcome.EXACT_MATCH)
ScoringConfig.score_meanings()  # complete dict[float, str]
```

---

## Reaction-center database

ChemCensor downloads the current database from
[Hugging Face](https://huggingface.co/datasets/insilicomedicine/chemcensor)
automatically on first use and reuses the Hugging Face cache afterward:

```python
from chemcensor import ChemCensor

censor = ChemCensor.open()
score = censor.score("CCO.CC(=O)O>>CCOC(=O)C")
```

The current database is `ChemCensor-DB-U3.sqlite` and requires
ChemCensor 1.3.0 or newer. The previous
`ChemCensor-DB-U2-1.0.0.sqlite.zip` database is retained for ChemCensor
1.0.0–1.2.x only.

| Database | Compatible ChemCensor versions |
| --- | --- |
| `ChemCensor-DB-U3.sqlite` | `>=1.3.0` |
| `ChemCensor-DB-U2-1.0.0.sqlite.zip` | `>=1.0.0,<1.3.0` |

To download explicitly:

```python
from chemcensor import download_default_database

db_path = download_default_database()
```

Or with the Hugging Face CLI:

```bash
hf download insilicomedicine/chemcensor \
  ChemCensor-DB-U3.sqlite \
  --repo-type dataset \
  --local-dir data
```

An explicit local path still works:

```python
censor = ChemCensor.open("data/ChemCensor-DB-U3.sqlite")
```

When a database contains build metadata, inspect it with:

```python
from chemcensor.db import DBManager

DBManager.read_metadata("data/ChemCensor-DB-U3.sqlite")
```

---

## Usage

The examples below use the automatically downloaded current database.

### Single reaction (in-process)

```python
from chemcensor import ChemCensor, ChemCensorConfig

censor = ChemCensor.open()
score = censor.score("CCO.CC(=O)O>>CCOC(=O)C")
```

`ChemCensor.open()` downloads the default database when needed and opens it
directly in immutable, read-only mode. Pass a local path to override it. The legacy
`ChemCensor(db_path=path)` API still copies it into an in-memory writable
connection.

Configure scoring and processing explicitly when needed:

```python
censor = ChemCensor.open(
    config=ChemCensorConfig(
        max_center_type=4,
        find_exact_match=True,
        check_functional_groups=True,
        validate_input=True,
        check_skeleton_conservation=True,
        check_static_stereo=True,
        use_cpu=False,
    ),
)
```

Calls to `evaluate*`, `score*`, `trace()` and `trace_batch()` on one
`ChemCensor` instance are thread-safe and serialized. Different instances can
run independently.

### Both score variants in one pass

`evaluate()` runs the (expensive) pipeline once and returns a `ScoreResult`
with both the functional-group aware and agnostic scores:

```python
from chemcensor import ChemCensor, ScoreResult

censor = ChemCensor.open()
result: ScoreResult = censor.evaluate("CCO.CC(=O)O>>CCOC(=O)C")

result.with_functional_groups        # score requiring FG sub-signature match
result.without_functional_groups     # score on reaction-center presence only
result.select(check_functional_groups=False)  # pick one by flag
result.all_fgs_precedents_are_real
result.all_center_precedents_are_real

if result.failure_reason is not None:
    result.failure_reason.stage
    result.failure_reason.category
    result.failure_reason.message
```

### Explainable scoring trace

`trace()` follows the same scoring path while retaining center coverage,
functional-group evidence and representative precedent reactions:

```python
trace = censor.trace("CCO.CC(=O)O>>CCOC(=O)C")

trace.result
trace.outcome
trace.chain_failed_at
trace.exact_real_precedents

for center in trace.centers:
    center.center_type
    center.reaction_center_smiles
    center.precedent_status
    center.required_functional_groups
    center.missing_functional_groups
    center.real_precedents
    center.virtual_precedents
    center.functional_group_evidence
```

Use `trace_batch([...])` to map and explain a route in one batch.

### Batch scoring in parallel (in-process)

```python
from chemcensor.parallel import score_batch, ParallelConfig

# list[ScoreResult], aligned with input order
results = score_batch(["CCO.CC(=O)O>>CCOC(=O)C", "A>>B"])
results[0].with_functional_groups

# or dict[int, ScoreResult] keyed by input position
as_dict = score_batch(smiles, return_dict=True)
```

Small batches reuse a guarded in-process scorer. Larger batches use the
multiprocessing pipeline. Configure the boundary with
`ParallelConfig(in_process_batch_threshold=N)` or set it to `0` to force
multiprocessing. Call `release_in_process_scorer()` to release the cached
mapper and its model allocations.

### Scoring a CSV file

`score_file` streams results to an output CSV with the columns
`idx, smiles, score_with_fg, score_without_fg`,
precedent provenance fields and structured failure fields. Rows are written as
workers complete them (not input order) — sort by `idx` if needed.

```python
from chemcensor.parallel import score_file, ParallelConfig

score_file(
    input_path="in.csv",
    output_path="out.csv",
    smiles_column="reaction_smiles",
    config=ParallelConfig(n_workers=8),  # None = autoscale to CPU count
    checkpoint_path="run.ckpt",          # optional, enables resume
)
```

Or from the command line:

```bash
python scripts/score_parallel.py in.csv out.csv
```

Useful flags: `--workers N`, `--mappers N`, `--cpu`,
`--smiles-column NAME`, `--checkpoint run.ckpt`,
`--fake-mapper` (reuse precomputed atom maps instead of running rxnmapper),
`--no-exact-match`, `--max-center-type {1,2,3,4}`.

---

## Building the reaction-center database

Compose a database from a reference CSV of reactions:

```bash
python scripts/compose_database.py reactions.csv rc_db.db \
    --db-version MY-DB-1 \
    --reaction-smiles-column cleaned_rxn \
    --document-id-column PatentNumber
```

For large inputs, use the parallel composer:

```bash
python scripts/compose_database_parallel.py reactions.csv rc_db.db \
    --db-version MY-DB-1 \
    --reaction-smiles-column cleaned_rxn \
    --document-id-column PatentNumber \
    --save-mapped
```

Databases composed with ChemCensor 1.2.2 or older use the earlier RC1 key
format and must be recomposed for complete stereo-aware RC1 matching. A
compatible unstamped database can be stamped with:

```bash
python scripts/stamp_database.py --db-path rc_db.db --db-version MY-DB-1
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
