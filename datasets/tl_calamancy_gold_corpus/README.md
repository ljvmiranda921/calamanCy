<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Benchmarking gold-annotated TLUnified data

## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[spaCy projects documentation](https://spacy.io/usage/projects).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `preprocess` | Preprocess the raw annotated data and convert into spaCy format. |
| `pretrain` | Pretrain with information from raw text |
| `init-fasttext` | Initialize fastText vectors. |
| `train` | Train the NER model. Usually called within the `benchmark.py` script. |
| `evaluate` | Evaluate NER model. Usually called within the `benchmark.py` script. |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `all` | `preprocess` &rarr; `train` &rarr; `evaluate` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/tl_tlunified_gold_v1.0.jsonl` | URL | Annotated TLUnified dataset. |
| `assets/tlunified.zip` | URL | TLUnified dataset (from Improving Large-scale Language Models and Resources for Filipino by Cruz and Cheng 2022). |
| `assets/fasttext.tl.gz` | URL | Tagalog fastText vectors provided from the fastText website (trained from CommonCrawl and Wikipedia). |
| `assets/tlunified_raw_text.jsonl` | URL | Pre-converted raw text from TLUnified in JSONL format (1.1 GB). |
| `assets/tl_tlunified_pt.bin` | Local | Pretraining weights for Tagalog using spaCy's pretrain command. |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->