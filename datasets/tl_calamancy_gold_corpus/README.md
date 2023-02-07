<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Benchmarking gold-annotated TLUnified data

This project performs structured evaluation for a gold-annotated Tagalog
dataset. I first annotated the silver-standard annotations from WikiANN to
produce gold-standard data. After three months of annotation, I obtained 7k+
samples with Person (PER), Organization (ORG), and Location (LOC) entities:

| Tagalog Data    | Documents | Tokens | PER  | ORG  | LOC  |
|-----------------|-----------|--------|------|------|------|
| Training Set    | 6252      | 198588 | 6418 | 3121 | 3296 |
| Development Set | 782       |  25007 |  793 |  392 |  409 |
| Test Set        | 782       |  25153 |  818 |  423 |  438 |

Then, I benchmarked word vector and transformer-based spaCy pipelines in
different settings (e.g., with or without pretraining, fastText/floret static
vectors, etc.). 

Finally, I came up with a (1) word vector-based pipeline that consists of
[floret vectors](https://github.com/explosion/floret) and [tok2vec weight
pretraining](https://spacy.io/usage/embeddings-transformers#pretraining)
(`tl_tlunified_lg`) and a (2) transformer-based pipeline using
[roberta-tagalog-large](https://huggingface.co/jcblaise/roberta-tagalog-large)
(`tl_tlunified_trf`). The results are shown below:

| Pipeline                 | Precision       | Recall          | F1-score        |
|--------------------------|-----------------|-----------------|-----------------|
| tl_tlunified_lg          | 0.85 (0.01)     | 0.86 (0.02)     | 0.86 (0.02)     |
| tl_tlunified_trf (base)  | 0.87 (0.02)     | 0.87 (0.01)     | 0.87 (0.01)     |
| tl_tlunified_trf (large) | 0.89 (0.01)     | 0.89 (0.00)     | 0.90 (0.02)     |

You can find the full write-up in my blog post, [*Towards a Tagalog NLP
Pipeline*](https://ljvmiranda921.github.io/notebook/2023/02/04/tagalog-pipeline/),
where I discuss my annotation process, architectural decisions, and
performance evaluation.


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
| `preprocess` | Preprocess the raw annotated data and convert into spaCy format. |
| `pretrain` | Pretrain with information from raw text |
| `build-floret` | Build floret binary for training fastText and floret vectors. |
| `train-vectors` | Train word vectors using the floret binary. |
| `init-vectors` | Initialize word vectors. |
| `setup-ner` | Prepare the Tagalog NER corpus, vectors, and pretrained weights. |
| `train-ner` | Train the NER model. Usually called within the `benchmark.py` script. |
| `train-ner-trf` | Train a transformer NER model. Usually called within the `benchmark.py` script. |
| `evaluate-ner` | Evaluate NER model. Usually called within the `benchmark.py` script. |
| `summarize-results` | Summarize results for a given experimental run. |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `ner-trf` | `setup-ner` &rarr; `train-ner-trf` &rarr; `evaluate-ner` |
| `ner` | `setup-ner` &rarr; `train-ner` &rarr; `evaluate-ner` |
| `vectors` | `build-floret` &rarr; `train-vectors` &rarr; `init-vectors` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/corpus.tar.gz` | URL | Annotated TLUnified corpora in spaCy format with train, dev, and test splits. |
| `assets/tl_tlunified_pt_chars.bin` | URL | Pretraining weights for Tagalog using spaCy's pretrain command (using 'characters' objective). |
| `assets/tl_tlunified_pt_vects.bin` | URL | Pretraining weights for Tagalog using spaCy's pretrain command (using 'vectors' objective). |
| `assets/tl_tlunified_pt_chars_floret.bin` | URL | Pretraining weights for Tagalog using spaCy's pretrain command (using 'characters' objective) and floret vectors. |
| `assets/vectors.tar.gz` | URL | spaCy-compatible fastText and floret vectors. |
| `assets/fasttext.tl.gz` | URL | Tagalog fastText vectors provided from the fastText website (trained from CommonCrawl and Wikipedia). |
| `assets/tl_tlunified_gold_v1.0.jsonl` | URL | Annotated TLUnified dataset. |
| `assets/tlunified.zip` | URL | TLUnified dataset (from Improving Large-scale Language Models and Resources for Filipino by Cruz and Cheng 2022). |
| `assets/tlunified_raw_text.jsonl` | URL | Pre-converted raw text from TLUnified in JSONL format (1.1 GB). |
| `assets/floret` | Git | Floret repository for training floret and fastText models. |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->