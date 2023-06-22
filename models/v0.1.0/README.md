<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Release v0.1.0

This is a spaCy project that trains the v0.1.0 models for calamanCy. You can
use this project to replicate the pipelines shipped by the project. First, you need to install the
required dependencies:

```
pip install -r requirements.txt
```

Then you need to download all the assets (corpora, static vectors, etc.) via:

```
python -m spacy project assets
```

Before training the pipelines, you first need to run the setup workflow. This step prepares the
corpora for training (or pretraining) and builds the necessary binaries for other downstream commands.

```
python -m spacy project run setup
```

You can then train a pipeline by passing its name to the spaCy project command. For example, if you wish to train
`tl_calamancy_md`, you can execute the corresponding workflow like so:

```
python -m spacy project run tl-calamancy-md 
```


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
| `setup-training-data` | Prepare the Tagalog corpora used for training various spaCy components |
| `setup-pretraining-data` | Prepare the Tagalog corpora used for self-supervised learning operations |
| `setup-fasttext-vectors` | Make fastText vectors spaCy compatible |
| `build-floret` | Build floret binary for training fastText / floret vectors |
| `train-vectors-md` | Train medium-sized word vectors (200 dims, 50k keys) using the floret binary. |
| `train-vectors-lg` | Train large-sized word vectors (200 dims, 200k keys) using the floret binary. |
| `pretrain-md` | Pretrain with information from raw text using floret (md) vectors |
| `pretrain-lg` | Pretrain with information from raw text using fastText vectors |
| `train-parser-tagger` | Train the parser and tagger components using the Universal Dependencies Ugnayan Treebank |
| `train-ner-md` | Train NER component of tl_calamancy_md using floret vectors with pretraining (50k unique vectors) |
| `train-ner-lg` | Train NER component of tl_calamancy_lg using fastText vectors with pretraining (714k unique keys) |
| `train-ner-trf` | Train NER component of tl_calamancy_trf using context-sensitive vectors from roberta-tagalog |
| `assemble-trf` | Assemble the tl_calamancy_trf model and package it as a spaCy pipeline |
| `assemble-lg` | Assemble the tl_calamancy_lg model and package it as a spaCy pipeline |
| `assemble-md` | Assemble the tl_calamancy_md model and package it as a spaCy pipeline |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `setup` | `setup-training-data` &rarr; `setup-pretraining-data` &rarr; `setup-fasttext-vectors` &rarr; `build-floret` |
| `tl-calamancy-trf` | `train-parser-tagger` &rarr; `train-ner-trf` &rarr; `assemble-trf` |
| `tl-calamancy-lg` | `pretrain-lg` &rarr; `train-vectors-lg` &rarr; `train-parser-tagger` &rarr; `train-ner-lg` &rarr; `assemble-lg` |
| `tl-calamancy-md` | `pretrain-md` &rarr; `train-vectors-md` &rarr; `train-parser-tagger` &rarr; `train-ner-md` &rarr; `assemble-md` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/corpus.tar.gz` | URL | Annotated TLUnified corpora in spaCy format with train, dev, and test splits. |
| `assets/treebank` | Git | Treebank data for UD_Tagalog-Ugnayan |
| `assets/fasttext.tl.gz` | URL | Tagalog fastText vectors provided from the fastText website (trained from CommonCrawl and Wikipedia). |
| `assets/tlunified.zip` | URL | TLUnified dataset (from Improving Large-scale Language Models and Resources for Filipino by Cruz and Cheng 2022). |
| `assets/floret` | Git | Floret repository for training floret and fastText models. |
| `assets/tlunified_raw_text.jsonl` | URL | Pre-converted raw text from TLUnified in JSONL format (1.1 GB). |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->