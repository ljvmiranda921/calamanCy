<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Reproducing TLUnified-NER benchmarks

This is a spaCy project that benchmarks TLUnified-NER on a variety of pipelines.
You can use this project to reproduce the experiments in the write-up. 
First, you need to install the required dependencies:

```
pip install -r requirements.txt
```

This step installs [spaCy](https://spacy.io) that allows you to access its command-line interface.  
Now run the set-up commands:

```
python -m spacy project assets
python -m spacy project run setup
```

> **Note**
> Some commands may take some time to run. 
> This is especially true for the transformer training and evaluation pipelines.
> I highly recommend running these on at least a T4 GPU (available on Colab Pro+) for faster runtimes.

The Python scripts in the `scripts/` directory are supposed to be standalone command-line applications. 
You should be able to use them independently from one another.


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
| `analyze` | Get dataset statistics for TLUnified-NER |
| `plot` | Create plots for the report |
| `baseline` | Train a transition-based parser without any embeddings or static vectors |
| `static-vectors` | Use the trained calamanCy pipeline to evaluate the dev and test set |
| `trf-monolingual` | Use the trained transformer-based calamanCy pipeline to evaluate the dev and test set |
| `trf-multilingual` | Train and evaluate multilingual model and evaluate the dev and test sets |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `setup` | `install-models` &rarr; `process-datasets` |
| `benchmark` | `baseline` &rarr; `static-vectors` &rarr; `trf-monolingual` &rarr; `trf-multilingual` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/tlunified_ner.tar.gz` | URL | Contains the annotated TLUnified corpora in spaCy format with PER, ORG, LOC as entity labels (named entity recognition). Annotated by three annotators with IAA (Cohen's Kappa) of 0.78. Corpora was based from *Improving Large-scale Language Models and Resources for Filipino* by Cruz and Cheng (2021). |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->