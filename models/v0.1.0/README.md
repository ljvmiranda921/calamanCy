<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Release v0.1.0

This is a spaCy project that trains the v0.1.0 models for calamanCy.


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
| `setup` | Prepare the Tagalog corpora and word vectors |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `tl-calamancy-trf` | `setup` |
| `tl-calamancy-lg` | `setup` |
| `tl-calamancy-md` | `setup` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/corpus.tar.gz` | URL | Annotated TLUnified corpora in spaCy format with train, dev, and test splits. |
| `assets/vectors.tar.gz` | URL | spaCy-compatible fastText and floret vectors. |
| `assets/fasttext.tl.gz` | URL | Tagalog fastText vectors provided from the fastText website (trained from CommonCrawl and Wikipedia). |
| `assets/tl_tlunified_pt_chars.bin` | URL | Pretraining weights for Tagalog using spaCy's pretrain command (using 'characters' objective). |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->