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

This step downloads all the necessary datasets and models for benchmarking
use. You can then run one of the [workflows](#-) below. They are organized by
task and a dataset identifier.


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
| `pretrain-hatespeech` | Pretrain on Hatespeech training data to initialize vectors |
| `train-hatespeech` | Train binary textcat on Hatespeech dataset |
| `train-hatespeech-trf` | Train binary textcat on Hatespeech dataset using transformers |
| `evaluate-hatespeech` | Evaluate binary textcat on Hatespeech test data |
| `pretrain-dengue` | Pretrain on Dengue training data to initialize vectors |
| `train-dengue` | Train multilabel textcat on Dengue dataset |
| `train-dengue-trf` | Train multilabel textcat on Dengue dataset using transformers |
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
| `textcat-hatespeech` | `pretrain-hatespeech` &rarr; `train-hatespeech` &rarr; `train-hatespeech-trf` &rarr; `evaluate-hatespeech` |
| `textcat_multilabel-dengue` | `pretrain-dengue` &rarr; `train-dengue` &rarr; `train-dengue-trf` &rarr; `evaluate-dengue` |
| `ner-calamancy_gold` | `evaluate-calamancy` |
| `parser-ud` | `evaluate-ud` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/treebank/UD_Tagalog-Ugnayan/` | Git | Treebank data for UD_Tagalog-Ugnayan. Originally sourced from *Parsing in the absence of related languages: Evaluating low-resource dependency parsers in Tagalog* by Aquino and de Leon (2020). |
| `assets/treebank/UD_Tagalog-TRG/` | Git | Treebank data for UD_Tagalog-TRG. Originally sourced from the thesis, *A treebank prototype for Tagalog*, at the University of Tübingen by Samson (2018). |
| `assets/hatespeech.zip` | URL | Contains 10k tweets with 4.2k testing and validation data labeled as hate speech or non-hate speech (text categorization). Based on *Monitoring dengue using Twitter and deep learning techniques* by Livelo and Cheng (2018). |
| `assets/dengue.zip` | URL | Contains tweets on dengue labeled with five different categories. Tweets can be categorized to multiple categories at the same time (multilabel text categorization). Based on *Hate speech in Philippine election-related tweets: Automatic detection and classification using natural language processing* by Cabasag et al. (2019) |
| `assets/calamancy_gold.tar.gz` | URL | Contains the annotated TLUnified corpora in spaCy format with PER, ORG, LOC as entity labels (named entity recognition). Annotated by three annotators with IAA (Cohen's Kappa) of 0.78. Corpora was based from *Improving Large-scale Language Models and Resources for Filipino* by Cruz and Cheng (2021). |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->