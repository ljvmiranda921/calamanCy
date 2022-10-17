<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Creating a silver-annotated dataset from WikiText-TL-39

This project creates a silver-annotated dataset for named-entity recognition
(NER). It uses another silver-annotated
[WikiANN](https://huggingface.co/datasets/wikiann) (`wikiann`) dataset to
train an initial NER model, and then bootstrapped the annotations of a
larger [WikiText-TL-39](https://huggingface.co/datasets/wikitext_tl39) corpus
(`wikitext-tl-39`).

This results to two NER models, one from the original WikiANN corpus
(`tl_wikiann_silver`) and another from the WikiText-TL-39 corpus
(`tl_wikitext_silver`). Evaluation is done by testing these models in a small
sample of gold annotations done by a native speaker.


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
| `download` | Download the WikiANN and WikIText-TL-39 datasets from Huggingface |
| `train-wikiann` | Train a Tagalog NER model from the WikiANN dataset |
| `annotate-silver` | Annotate a larger WikiText-TL-39 dataset using the trained model from WikiANN |
| `train-wikitext` | Train a Tagalog NER model from the WikiText dataset |
| `evaluate-wikiann` | Evaluate the trained models to the silver-annotated WikiANN test set |
| `evaluate-wikitext` | Evaluate the trained models to the silver-annotated WikiText test set |
| `evaluate-gold` | Evaluate the trained models on an annotated subset of WikiText TL-39 |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `all` | `download` &rarr; `train-wikiann` &rarr; `annotate-silver` &rarr; `train-wikitext` &rarr; `evaluate-wikiann` &rarr; `evaluate-wikitext` &rarr; `evaluate-gold` |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->