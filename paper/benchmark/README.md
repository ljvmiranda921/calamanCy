<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Benchmarking project for calamanCy

This is a spaCy project that benchmarks calamanCy on a variety of tasks.
You can use this project to reproduce the experiments in the write-up. First, 
you need to install the required dependencies:

```
pip install -r requirements.txt
```

Then run the set-up commands:

```
python -m spacy project assets
python -m spacy project run setup
```

This step downloads all the necessary datasets and models for benchmarking use.


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
| `install-models` | Install models in the spaCy workspace |
| `process-datasets` | Process the datasets and convert them into spaCy format |
| `train-hatespeech` | Train binary textcat on Hatespeech dataset |
| `evaluate-hatespeech` | Evaluate binary textcat on Hatespeech test data |
| `train-dengue` | Train multilabel textcat on Dengue dataset |
| `evaluate-dengue` | Evaluate multilabel textcat on Dengue test data |
| `evaluate-calamancy` | Evaluate ner on calamanCy gold dev and test data |
| `evaluate-ud` | Evaluate parser and tagger on the combined Tagalog treebanks |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `setup` | `install-models` &rarr; `process-datasets` |
| `textcat-hatespeech` | `train-hatespeech` &rarr; `evaluate-hatespeech` |
| `textcat_multilabel-dengue` | `train-dengue` &rarr; `evaluate-dengue` |
| `ner-calamancy_gold` | `evaluate-calamancy` |
| `parser-ud` | `evaluate-ud` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/hatespeech.tar.gz` | URL | Contains 10k tweets with 4.2k testing and validation data labeled as hate speech or non-hate speech (text categorization). Based on *Monitoring dengue using Twitter and deep learning techniques* by Livelo and Cheng (2018). |
| `assets/dengue.tar.gz` | URL | Contains tweets on dengue labeled with five different categories. Tweets can be categorized to multiple categories at the same time (multilabel text categorization). Based on *Hate speech in Philippine election-related tweets: Automatic detection and classification using natural language processing* by Cabasag, Chen, et al. (2019) |
| `assets/calamancy_gold.tar.gz` | URL | Contains the annotated TLUnified corpora in spaCy format with PER, ORG, LOC as entity labels (named entity recognition). |
| `assets/treebank/UD_Tagalog-Ugnayan/` | Git | Treebank data for UD_Tagalog-Ugnayan |
| `assets/treebank/UD_Tagalog-TRG/` | Git | Treebank data for UD_Tagalog-TRG |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->