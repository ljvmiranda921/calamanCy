<!-- WEASEL: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 Weasel Project: Release v0.2.0

This is a spaCy project that trains the v0.2.0 models for calamanCy.
Here are some of the major changes in this release:

- **Included trainable lemmatizer in the pipeline**: instead of a rules-based
lemmatizer, we are now using the [neural edit-tree
lemmatizer](https://explosion.ai/blog/edit-tree-lemmatizer).
- **Trained on UD-NewsCrawl**: this is a major update, as we are now training
our parser, tagger, and morphologizer components on the larger
[UD-NewsCrawl](https://huggingface.co/datasets/UD-Filipino/UD_Tagalog-NewsCrawl)
treebank.  Our training dataset has now increased from 150+ to 15,000! From
this point forward, we will be using the UD-TRG and UD-Ugnayan treebanks as
test sets (as intended).
- **Better evaluations**: Aside from evaluating our dependency parser and POS tagger on UD-TRG and UD-Ugnayan, we have also included Universal NER ([Mayhew et al., 2023](https://arxiv.org/abs/2311.09122)) as our test set for evaluating the NER component.
- **Improved base model for tl_calamancy_trf**: Based on internal evaluations, we are now using [mDeBERTa-v3 (base)](https://huggingface.co/microsoft/mdeberta-v3-base) as our source of context-sensitive vectors for tl_calamancy_trf.
- **Simpler pipelines, no more pretraining**: We found that pretraining doesn't really offer huge performance gains (0-1%) given the huge effort and time needed to do it. Hence, for ease of training the whole pipeline, we removed it from the calamanCy recipe.

The namespaces for the latest models remain the same.
The legacy models will have an explicit version number in their HuggingFace repositories.
Please see [this HuggingFace collection](https://huggingface.co/collections/ljvmiranda921/calamancy-models-for-tagalog-nlp-65629cc46ef2a1d0f9605c87) for more information.

## Set-up

You can use this project to replicate the pipelines shipped by the project.
First, you need to install the required dependencies:

```sh
pip install -r requirements.txt
```

Then run the set-up commands:

```sh
python -m spacy project assets
python -m spacy project run setup
```

This step downloads all assets and prepares all the datasets and binaries for
training use. For example, if you want to train `tl_calamancy_md`, run the following comand:

```sh
MODEL=tl_calamancy_md scripts/train.sh
```


## Model information

The table below shows an overview of the calamanCy models in this project. For more information,
I suggest checking the [language pipeline metadata](https://spacy.io/api/language#meta).


| Model                       | Pipelines                                   | Description                                                                                                  |
|-----------------------------|---------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| tl_calamancy_md (214 MB)   | tok2vec, tagger, trainable_lemmatizer, morphologizer, parser, ner | CPU-optimized Tagalog NLP model. Pretrained using the TLUnified dataset. Using floret vectors (50k keys)     |
| tl_calamancy_lg (482 MB)  | tok2vec, tagger, trainable_lemmatizer, morphologizer, parser, ner | CPU-optimized large Tagalog NLP model. Pretrained using the TLUnified dataset. Using fastText vectors (714k) |
| tl_calamancy_trf (1.7 GB) | transformer, tagger, trainable_lemmatizer, morphologizer, parser, ner            | GPU-optimized transformer Tagalog NLP model. Uses mdeberta-v3-base as context vectors.                   |


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
| `setup-finetuning-data` | Prepare the Tagalog corpora used for training various spaCy components |
| `setup-fasttext-vectors` | Make fastText vectors spaCy compatible |
| `build-floret` | Build floret binary for training fastText / floret vectors |
| `train-vectors-md` | Train medium-sized word vectors (200 dims, 200k keys) using the floret binary. |
| `train-parser` | Train a trainable_lemmatizer, parser, tagger, and morphologizer using the Universal Dependencies treebanks |
| `train-parser-trf` | Train a trainable_lemmatizer, parser, tagger, and morphologizer using the Universal Dependencies treebanks |
| `train-ner` | Train ner component |
| `train-ner-trf` | Train ner component |
| `assemble` | Assemble pipelines to create a single spaCy piepline |
| `assemble-trf` | Assemble pipelines to create a single spaCy piepline |
| `setup-eval-data` | Convert remaining test datasets |
| `evaluate-model` | Evaluate a model |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`weasel run [name]`](https://github.com/explosion/weasel/tree/main/docs/cli.md#rocket-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `setup` | `setup-finetuning-data` &rarr; `setup-fasttext-vectors` &rarr; `build-floret` &rarr; `train-vectors-md` |
| `tl-calamancy` | `train-parser` &rarr; `train-ner` &rarr; `assemble` |
| `tl-calamancy-trf` | `train-parser-trf` &rarr; `train-ner-trf` &rarr; `assemble-trf` |
| `evaluate` | `setup-eval-data` &rarr; `evaluate-model` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`weasel assets`](https://github.com/explosion/weasel/tree/main/docs/cli.md#open_file_folder-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/tlunified_raw_text.txt` | URL | Pre-converted raw text from TLUnified in JSONL format (1.1 GB). |
| `assets/corpus.tar.gz` | URL | Annotated TLUnified corpora in spaCy format with train, dev, and test splits. |
| `assets/tl_newscrawl-ud-train.conllu` | URL | Train dataset for NewsCrawl |
| `assets/tl_newscrawl-ud-dev.conllu` | URL | Dev dataset for NewsCrawl |
| `assets/tl_newscrawl-ud-test.conllu` | URL | Test dataset for NewsCrawl |
| `assets/tl_trg-ud-test.conllu` | URL | Test dataset for TRG |
| `assets/tl_ugnayan-ud-test.conllu` | URL | Test dataset for Ugnayan |
| `assets/uner_trg.iob2` | URL | Test dataset for Universal NER TRG |
| `assets/uner_ugnayan.iob2` | URL | Test dataset for Universal NER Ugnayan |
| `assets/tfnerd.txt` | URL | Test dataset for TF-NERD |
| `assets/fasttext.tl.gz` | URL | Tagalog fastText vectors provided from the fastText website (trained from CommonCrawl and Wikipedia). |
| `assets/floret` | Git | Floret repository for training floret and fastText models. |

<!-- WEASEL: AUTO-GENERATED DOCS END (do not remove) -->
