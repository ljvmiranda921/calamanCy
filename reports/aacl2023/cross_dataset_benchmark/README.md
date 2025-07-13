<!-- WEASEL: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 Weasel Project: Cross-dataset benchmarks

This is a spaCy project for additional cross-dataset experiments for the paper.
I decided to separate them from the other `benchmarks/` directory for easier organization.
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

Let's say we want to train a model from WikiANN and evaluate it to TLUnified, we simply need to run the following command:

```
python -m spacy project run all . --vars.train_dev wikiann --vars.test tlunified
# If vice-versa (note that we should use the corrected version):
python -m spacy project run all . --vars.train_dev tlunified --vars.test wikiann_corrected
```

This should train all models from a transition-based parser NER (baseline) to mono/multilingual LMs.
It is also possible to train a specific model by passing the correct command (e.g., `baseline`, `static-vectors`, etc.)
You can find the results in the `metrics/` directory.


## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[Weasel documentation](https://github.com/explosion/weasel).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`weasel run [name]`](https://github.com/explosion/weasel/tree/main/docs/cli.md#rocket-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `process-datasets` | Process the datasets and convert them into spaCy format |
| `baseline` | Train a transition-based parser without any embeddings or static vectors |
| `static-vectors` | Use fastText vectors to initialize an NER model |
| `trf-monolingual` | Train and evaluate monolingual transformer model. |
| `trf-multilingual` | Train and evaluate multilingual transformer model |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`weasel run [name]`](https://github.com/explosion/weasel/tree/main/docs/cli.md#rocket-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `setup` | `process-datasets` |
| `all` | `baseline` &rarr; `static-vectors` &rarr; `trf-monolingual` &rarr; `trf-multilingual` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`weasel assets`](https://github.com/explosion/weasel/tree/main/docs/cli.md#open_file_folder-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/tlunified_ner.tar.gz` | URL | Contains the annotated TLUnified corpora in spaCy format with PER, ORG, LOC as entity labels (named entity recognition). Annotated by three annotators with IAA (Cohen's Kappa) of 0.78. Corpora was based from *Improving Large-scale Language Models and Resources for Filipino* by Cruz and Cheng (2021). |
| `assets/fasttext.tl.gz` | URL | Tagalog fastText vectors provided from the fastText website (trained from CommonCrawl and Wikipedia). |

<!-- WEASEL: AUTO-GENERATED DOCS END (do not remove) -->
