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
task and a dataset identifier (e.g., `textcat-hatespeech`,
`textcat_multilabel-dengue`).

## Benchmarking results

We benchmarked on the following datasets by training the pipeline on the train
and development data and evaluating on a held-out test set. We did this for
five (5) trials and we report their average. Since the combined treebank has
little data, we opted to evaluate it using k-fold cross-validation:

- **Hatespeech** (Cabasag et al., 2019): a binary text categorization task that contains 10k tweets labeled as hate speech or non hate speech. We report the macro F1-score on the test set.
- **Dengue** (Livelo and Cheng, 2018): a multilabel text categorization task that contains dengue-related tweets across five labels: *absent*, *dengue*, *health*, and *mosquito*. We report the macro F1-score on the test set.
- **calamanCy gold**: an annotated version of the TLUnified dataset (Cruz and Cheng, 2021). Labeled by three annotators across a four-month period with an IAA (Cohen's Kappa) of 0.78. We report the F1-score on the test set.
- **Merged UD**: a merged version of the Ugnayan (Aquino and de Leon, 2020) and TRG  (Samson, 2018) treebanks. We shuffled the two treebanks after merging and evaluated via 10-fold cross validation. We report both UAS and LAs results.

| Language Pipeline      | Binary text categorization, macro F1-score (Hatespeech) | Multilabel text categorization, macro F1-score (Dengue)  | Named entity recognition, F1-score (calamanCy Gold) | Dependency parsing, UAS (Merged UD) | Dependency parsing, LAS (Merged UD) |
|------------------------|---------------------------------------------------------|----------------------------------------------------------|-----------------------------------------------------|-------------------------------------|-------------------------------------|
| tl_calamancy_md-0.1.0  | 74.40 (0.05)                                            | 65.32 (0.04)                                             | 87.67 (0.03)                                        | 76.47                               | 54.40                               |
| tl_calamancy_lg-0.1.0  | 75.62 (0.02)                                            | 68.42 (0.01)                                             | 88.90 (0.01)                                        | 82.13                               | 60.32                               |
| tl_calamancy_trf-0.1.0 | 78.25 (0.06)                                            | 72.45 (0.02)                                             | 90.34 (0.02)                                        | 92.48                               | 80.92                               |


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
| `assets/hatespeech.zip` | URL | Contains 10k tweets with 4.2k testing and validation data labeled as hate speech or non-hate speech (text categorization). Based on *Hate speech in Philippine election-related tweets: Automatic detection and classification using natural language processing* by Cabasag et al. (2019) |
| `assets/dengue.zip` | URL | Contains tweets on dengue labeled with five different categories. Tweets can be categorized to multiple categories at the same time (multilabel text categorization). Based on *Monitoring dengue using Twitter and deep learning techniques* by Livelo and Cheng (2018). |
| `assets/calamancy_gold.tar.gz` | URL | Contains the annotated TLUnified corpora in spaCy format with PER, ORG, LOC as entity labels (named entity recognition). Annotated by three annotators with IAA (Cohen's Kappa) of 0.78. Corpora was based from *Improving Large-scale Language Models and Resources for Filipino* by Cruz and Cheng (2021). |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->