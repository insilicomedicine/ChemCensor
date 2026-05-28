# ChemCensor

[![Dataset](https://img.shields.io/badge/Dataset-Hugging%20Face-FFD21F?style=flat-square&logo=huggingface&logoColor=black)](https://huggingface.co/datasets/insilicomedicine/chemcensor)
[![Paper](https://img.shields.io/badge/Paper-arXiv%3A2602.03554-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2602.03554)

ChemCensor is a precedent-based framework for evaluating reaction chemical plausibility.
It separates the **reaction center** (what changes) from the **functional-group context** (what must be tolerated), then checks whether similar patterns are supported by known precedents stored in an SQLite database.

The resulting **ChemCensor Score** is an integer confidence level from 0 to 5, where higher values indicate stronger precedent support.

---

## Installation


```bash
python -m pip install -e .
```

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
