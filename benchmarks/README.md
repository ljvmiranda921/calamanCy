<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Benchmarking NER pipelines for gold-annotated Tagalog corpora

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
| `convert` | Convert raw annotations into spaCy files. |
| `raw-text` | Get raw text as preparation for pretraining |
| `init-fasttext` | Initialize fastText vectors. |
| `pretrain` | Pretrain with information from raw text |
| `train-ner` | Train NER model. |
| `evaluate` | Evaluate NER model. |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `ner` | `convert` &rarr; `train-ner` &rarr; `evaluate` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/tlunified.zip` | URL | TLUnified dataset (from Improving Large-scale Language Models and Resources for Filipino by Cruz and Cheng 2022) |
| `assets/fasttext.tl.gz` | URL | Tagalog fastText vectors |
| `assets/tlunified_pt_chars.bin` | Local | Pretrained weights (characters) from TLUnified using `baseline` config |
| `assets/tlunified_pt_vects.bin` | Local | Pretrained weights (vectors) from TLUnified using `fastText` config |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->