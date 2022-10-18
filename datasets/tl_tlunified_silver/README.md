<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Creating a silver-annotated dataset from TLUnified corpus

This project creates a silver-annotated dataset for named-entity recognition
(NER). It uses another silver-annotated
[WikiANN](https://huggingface.co/datasets/wikiann) (`wikiann`) dataset to
train an initial NER model, and then bootstrapped the annotations of a
larger [TLUnified](https://arxiv.org/abs/2111.06053) corpus
(`tlunified`).

For evaluation, I trained two NER models, one from the original WikiANN corpus
(`tl_wikiann_silver`) and another from the TLUnified corpus
(`tl_tlunified_silver`). I then tested them against a small sample of
tlunified's data annotated by me, a native speaker.


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
| `download` | Download the WikiANN and TLUnified datasets and save to spaCy format |
| `train-wikiann` | Train a Tagalog NER model from the WikiANN dataset |
| `annotate-silver` | Annotate a larger tlunified-TL-39 dataset using the trained model from WikiANN |
| `train-tlunified` | Train a Tagalog NER model from the tlunified dataset |
| `evaluate-wikiann` | Evaluate the trained models to the silver-annotated WikiANN test set |
| `evaluate-tlunified` | Evaluate the trained models to the silver-annotated tlunified test set |
| `evaluate-gold` | Evaluate the trained models on an annotated subset of tlunified |
| `package` | Package the trained models from the silver-annotated datasets |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `all` | `download` &rarr; `train-wikiann` &rarr; `annotate-silver` &rarr; `train-tlunified` &rarr; `evaluate-wikiann` &rarr; `evaluate-tlunified` &rarr; `evaluate-gold` &rarr; `package` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/tlunified.zip` | URL | TLUnified dataset (from Improving Large-scale Language Models and Resources for Filipino by Cruz and Cheng 2022) |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->