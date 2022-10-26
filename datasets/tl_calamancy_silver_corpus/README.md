<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Creating a silver-standard dataset from the TLUnified Tagalog corpus

This project creates, `tl_calamancy_silver_corpus` a silver-standard dataset for
named-entity recognition (NER). It uses another silver-annotated
[WikiANN](https://huggingface.co/datasets/wikiann) (`wikiann`) dataset to train an
initial NER model, and then bootstrapped the annotations of a larger
[TLUnified](https://arxiv.org/abs/2111.06053) corpus (`tlunified`).

### Evaluation

After bootstrapping the annotations of TLUnified with a model trained from
WikiANN,I split the dataset into train, dev, and test for different sizes
(10k, 30k, 50k). I did it this way because unfortunately, the bulk of the
TLUnified dataset cannot fit my machine's memory constraints.

Lastly, I trained a TLUnified model from these silver-standard annotations and
evaluated it on its own test set. I did this for five trials, reporting the mean 
and standard deviation. You can see the results below:

| Dataset Size              | ENTS_P      | ENTS_R      | ENTS_F      | SPEED (WPS)       |
|---------------------------|-------------|-------------|-------------|-------------------|
| tl_tlunified_silver-10000 | 0.59 (0.03) | 0.55 (0.03) | 0.57 (0.03) | 33809.12 (397.81) |
| tl_tlunified_silver-30000 | 0.67 (0.02) | 0.66 (0.01) | 0.66 (0.02) | 50477.00 (724.74) |
| tl_tlunified_silver-50000 | 0.70 (0.01) | 0.69 (0.03) | 0.70 (0.02) | 56460.42 (590.85) |

And here are the per-entity results:

| Dataset Size              | Entity | Precision   | Recall      | F-score     |
|---------------------------|--------|-------------|-------------|-------------|
| tl_tlunified_silver-10000 | LOC    | 0.57 (0.03) | 0.51 (0.04) | 0.54 (0.03) |
|                           | ORG    | 0.68 (0.07) | 0.66 (0.04) | 0.67 (0.05) |
|                           | PER    | 0.56 (0.05) | 0.50 (0.04) | 0.53 (0.03) |
| tl_tlunified_silver-30000 | LOC    | 0.64 (0.02) | 0.62 (0.02) | 0.63 (0.02) |
|                           | ORG    | 0.63 (0.04) | 0.62 (0.03) | 0.63 (0.03) |
|                           | PER    | 0.76 (0.04) | 0.76 (0.04) | 0.76 (0.02) |
| tl_tlunified_silver-50000 | LOC    | 0.65 (0.03) | 0.64 (0.04) | 0.65 (0.03) |
|                           | ORG    | 0.68 (0.02) | 0.66 (0.03) | 0.67 (0.02) |
|                           | PER    | 0.79 (0.02) | 0.80 (0.04) | 0.79 (0.02) |

In addition, I also created a small gold-standard test set to evaluate the
models against. The annotations were done by me, a native speaker, using
[Prodigy](https://prodi.gy). Here are the results:






### Future goal

My eventual goal for this project is to produce a gold-standard NER dataset
from TLUnified. This should help train more robust and performance Tagalog models
for structured prediction.


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
| `download-wikiann` | Download the WikiANN dataset from HuggingFace and save to spaCy format |
| `process-tlunified` | Convert the TLUnified dataset to the spaCy format |
| `train-wikiann` | Train a Tagalog NER model from the WikiANN dataset |
| `annotate-silver` | Annotate a larger TLUnified dataset using the trained model from WikiANN |
| `train-tlunified` | Train a Tagalog NER model from the tlunified dataset |
| `evaluate-wikiann` | Evaluate WikiANN to its test set |
| `evaluate-tlunified` | Evaluate TLUnified to its test set |
| `cross-evaluate-wikiann` | Evaluate the trained models to the silver-annotated WikiANN test set |
| `cross-evaluate-tlunified` | Evaluate the trained models to the silver-annotated tlunified test set |
| `cross-evaluate-gold` | Evaluate the trained models on an annotated subset of tlunified |
| `package` | Package the trained models from the silver-annotated datasets |
| `annotate` | Annotate the TLUnified dataset using Prodigy's ner.correct |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `all` | `download-wikiann` &rarr; `process-tlunified` &rarr; `train-wikiann` &rarr; `annotate-silver` &rarr; `train-tlunified` &rarr; `cross-evaluate-wikiann` &rarr; `cross-evaluate-tlunified` &rarr; `package` |
| `wikiann` | `download-wikiann` &rarr; `train-wikiann` &rarr; `evaluate-wikiann` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/tlunified.zip` | URL | TLUnified dataset (from Improving Large-scale Language Models and Resources for Filipino by Cruz and Cheng 2022) |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->