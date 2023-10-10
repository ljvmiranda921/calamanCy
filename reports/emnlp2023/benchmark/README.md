<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Reproducing calamanCy benchmarks

This is a spaCy project that benchmarks calamanCy on a variety of tasks.
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

This step downloads all the necessary datasets and models for benchmarking use. 
You can then run one of the [workflows](#-) below. 
They are organized by task and a dataset identifier (e.g., `textcat-hatespeech`, `textcat_multilabel-dengue`).
You can find the training configuration (i.e., hyperparameters, architectures, etc.) in the `configs/` directory.

> **Note**
> Some commands may take some time to run. 
> This is especially true for the transformer training and evaluation pipelines.
> I highly recommend running these on at least a T4 GPU (available on Colab Pro+) for faster runtimes.

The Python scripts in the `scripts/` directory are supposed to be standalone command-line applications. 
You should be able to use them independently from one another. 


## Benchmarking results

We benchmarked on the following datasets by training the pipeline on the train and development data and evaluating on a held-out test set. 
We did this for five (5) trials and we report their average. Since the combined treebank has little data, we opted to evaluate it using k-fold cross-validation:

- **Hatespeech** (Cabasag et al., 2019): a binary text categorization task that contains 10k tweets labeled as hate speech or non hate speech. We report the macro F1-score on the test set.
- **Dengue** (Livelo and Cheng, 2018): a multilabel text categorization task that contains dengue-related tweets across five labels: *absent*, *dengue*, *health*, and *mosquito*. We report the macro F1-score on the test set.
- **TLUnified-NER**: an annotated version of the TLUnified dataset (Cruz and Cheng, 2021). Labeled by three annotators across a four-month period with an IAA (Cohen's Kappa) of 0.78. We report the F1-score on the test set.
- **Merged UD**: a merged version of the Ugnayan (Aquino and de Leon, 2020) and TRG  (Samson, 2018) treebanks. We shuffled the two treebanks after merging and evaluated via 10-fold cross validation. We report both UAS and LAS results.

| Language Pipeline      | Binary text categorization, macro F1-score (Hatespeech) | Multilabel text categorization, macro F1-score (Dengue)  | Named entity recognition, F1-score (TLUnified-NER)  | Dependency parsing, UAS (Merged UD) | Dependency parsing, LAS (Merged UD) |
|------------------------|---------------------------------------------------------|----------------------------------------------------------|-----------------------------------------------------|-------------------------------------|-------------------------------------|
| tl_calamancy_md        | 74.40 (0.05)                                            | 65.32 (0.04)                                             | 87.67 (0.03)                                        | 76.47                               | 54.40                               |
| tl_calamancy_lg        | 75.62 (0.02)                                            | 68.42 (0.01)                                             | 88.90 (0.01)                                        | 82.13                               | 70.32                               |
| tl_calamancy_trf       | 78.25 (0.06)                                            | 72.45 (0.02)                                             | 90.34 (0.02)                                        | 92.48                               | 80.90                               |

We also evaluated cross-lingual and multilingual approaches in our benchmarks: 
- **Cross-lingual**: we chose the source languages using a WALS-reliant metric (Agic, 2017) to choose the linguistically-closest languages to Tagalog and looked for their corresponding spaCy pipelines. 
  We came up with Indonesian (id), Vietnamese (vi), Ukranian (uk), Romanian (ro), and Catalan (ca). However, only uk, ca, ro have spaCy pipelines. We finetuned each dataset for each task and evaluated them similarly to our Tagalog monolingual models.

| Language Pipeline      | Binary text categorization, macro F1-score (Hatespeech) | Multilabel text categorization, macro F1-score (Dengue)  | Named entity recognition, F1-score (TLUnified-NER)  | Dependency parsing, UAS (Merged UD) | Dependency parsing, LAS (Merged UD) |
|------------------------|---------------------------------------------------------|----------------------------------------------------------|-----------------------------------------------------|-------------------------------------|-------------------------------------|
| uk_core_news_trf       | 75.24 (0.05)                                            | 65.57 (0.01)                                             | 51.11 (0.02)                                        | 54.77                               | 82.86                               |
| ro_core_news_lg        | 69.01 (0.01)                                            | 59.10 (0.01)                                             | 02.01 (0.00)                                        | 84.65                               | 82.80                               |
| ca_core_news_trf       | 70.01 (0.02)                                            | 59.42 (0.03)                                             | 14.58 (0.02)                                        | 91.17                               | 83.09                               |

- **Multilingual**: we used XLM RoBERTa and an uncased version of mBERT as our base transformer models. We also finetuned each model for each task and did similar evaluations.
  Note that finetuning on XLM RoBERTa (both base and large versions) may require at least a V100 GPU. I've seen more consistent and stable training with an A100 GPU. Same can be said for mBERT.

| Language Pipeline      | Binary text categorization, macro F1-score (Hatespeech) | Multilabel text categorization, macro F1-score (Dengue)  | Named entity recognition, F1-score (TLUnified-NER)  | Dependency parsing, UAS (Merged UD) | Dependency parsing, LAS (Merged UD) |
|------------------------|---------------------------------------------------------|----------------------------------------------------------|-----------------------------------------------------|-------------------------------------|-------------------------------------|
| xlm-roberta-base       | 77.57 (0.01)                                            | 67.20 (0.01)                                             | 88.03 (0.03)                                        | 88.34                               | 76.07                               |
| bert-base-multilingual | 76.40 (0.02)                                            | 71.07 (0.04)                                             | 87.40 (0.02)                                        | 90.79                               | 78.52                               |


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
| `train-hatespeech-crosslingual` | Train crosslingual models for the Hatespeech dataset |
| `evaluate-hatespeech-crosslingual` | Evaluate crosslingual models for the Hatespeech dataset |
| `train-dengue-crosslingual` | Train crosslingual models for the Dengue dataset |
| `evaluate-dengue-crosslingual` | Evaluate crosslingual models for the Dengue dataset |
| `evaluate-calamancy-crosslingual` | Evaluate crosslingual models for the calamanCy gold test data |
| `evaluate-ud-crosslingual` | Evaluate parser and tagger on the combined Tagalog treebanks using crosslingual models |
| `train-hatespeech-multilingual` | Train multilingual models for the Hatespeech dataset |
| `evaluate-hatespeech-multilingual` | Evaluate multilingual models for the Hatespeech dataset |
| `train-dengue-multilingual` | Train multilingual models for the Dengue dataset |
| `evaluate-dengue-multilingual` | Evaluate multilingual models for the Dengue dataset |
| `train-calamancy-multilingual` | Finetune multilingual models for the calamanCy gold train and dev data |
| `evaluate-calamancy-multilingual` | Evaluate multilingual models for the calamanCy gold test data |
| `evaluate-ud-multilingual` | Evaluate parser and tagger on the combined Tagalog treebanks using multilingual models |

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
| `crosslingual` | `train-hatespeech-crosslingual` &rarr; `evaluate-hatespeech-crosslingual` &rarr; `train-dengue-crosslingual` &rarr; `evaluate-dengue-crosslingual` &rarr; `evaluate-calamancy-crosslingual` &rarr; `evaluate-ud-crosslingual` |
| `multilingual` | `train-hatespeech-multilingual` &rarr; `evaluate-calamancy-multilingual` &rarr; `train-dengue-multilingual` &rarr; `evaluate-dengue-multilingual` &rarr; `train-calamancy-multilingual` &rarr; `evaluate-calamancy-multilingual` &rarr; `evaluate-ud-multilingual` |

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