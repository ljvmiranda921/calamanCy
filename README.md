<img src="https://raw.githubusercontent.com/ljvmiranda921/calamanCy/master/logo.png" width="125" height="125" align="right" />

# calamanCy: NLP pipelines for Tagalog

[![GitHub workflow](https://github.com/ljvmiranda921/calamancy/actions/workflows/test.yml/badge.svg)](https://github.com/ljvmiranda921/calamanCy/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/calamancy?labelColor=%23272c32&color=%2333cc56&logo=pypi&logoColor=white)](https://pypi.org/project/calamanCy/)
[![Paper](https://img.shields.io/badge/read-EMNLP%20paper-blue?logo=semanticscholar)](https://www.semanticscholar.org/reader/598a4f17da8f4cddfab3c7c10bc96a05078e7a91)

**calamanCy** is a Tagalog natural language preprocessing framework made with
[spaCy](https://spacy.io). Its goal is to provide pipelines and datasets for
downstream NLP tasks. This repository contains material for using calamanCy,
reproduction of results, and guides on usage.

> calamanCy takes inspiration from other language-specific [spaCy Universe frameworks](https://spacy.io/universe) such as
> [DaCy](https://github.com/centre-for-humanities-computing/DaCy), [huSpaCy](https://github.com/huspacy/huspacy),
> and [graCy](https://github.com/jmyerston/graCy). The name is based from [_calamansi_](https://en.wikipedia.org/wiki/Calamansi),
> a citrus fruit native to the Philippines and used in traditional Filipino cuisine.

🌐 **Website**: [https://ljvmiranda921.github.io/calamanCy](https://ljvmiranda921.github.io/calamanCy)

## 📰 News

- [2024-08-01] Released new NER-only models based on [GLiNER](https://github.com/urchade/GLiNER)! You can find the models in [this HuggingFace collection](https://huggingface.co/collections/ljvmiranda921/calamancy-models-for-tagalog-nlp-65629cc46ef2a1d0f9605c87). Span-Marker and calamanCy models are still superior, but GLiNER offers a lot of extensibility on unseen entity labels. You can find the training pipeline [here](https://github.com/ljvmiranda921/calamanCy/tree/master/models/v0.1.0-gliner).
- [2024-07-02] I talked about calamanCy during my guest lecture, "Artisanal Filipino NLP Resources in the time of Large Language Models," @ DLSU Manila. You can find the slides (and an accompanying blog post) [here](https://ljvmiranda921.github.io/notebook/2024/07/02/talk-dlsu/).
- [2023-12-05] We released the paper [**calamanCy: A Tagalog Natural Language Processing Toolkit**](https://aclanthology.org/2023.nlposs-1.1/) and will be presented in the NLP-OSS workshop at EMNLP 2023! Feel free to check out the [Tagalog NLP collection in HuggingFace](https://huggingface.co/collections/ljvmiranda921/calamancy-models-for-tagalog-nlp-65629cc46ef2a1d0f9605c87).
- [2023-11-01] The named entity recognition (NER) dataset used to train the NER component of calamanCy has now a corresponding paper: [**Developing a Named Entity Recognition Dataset for Tagalog**](https://aclanthology.org/2023.nlposs-1.1/)! It will be presented in the SEALP workshop at IJCNLP-AACL 2023! The dataset is also available [in HuggingFace](https://huggingface.co/datasets/ljvmiranda921/tlunified-ner). I've also talked about my thoughts on the annotation process [in my blog](https://ljvmiranda921.github.io/notebook/2023/07/03/devlog-calamancy/).
- [2023-08-01] First release of calamanCy! Please check out [this blog post](https://ljvmiranda921.github.io/projects/2023/08/01/calamancy/) to learn more and read some of my preliminary work back in February [here](https://ljvmiranda921.github.io/notebook/2023/02/04/tagalog-pipeline/).

## 🔧 Installation

To get started with calamanCy, simply install it using `pip` by running the
following line in your terminal:

```sh
pip install calamanCy
```

### Development

If you are developing calamanCy, first clone the repository:

```sh
git clone git@github.com:ljvmiranda921/calamanCy.git
```

Then, create a virtual environment and install the dependencies:

```sh
python -m venv venv
venv/bin/pip install -e .  # requires pip>=23.0
venv/bin/pip install .[dev]

# Activate the virtual environment
source venv/bin/activate
```

or alternatively, use `make dev`.

### Running the tests

We use [pytest](https://docs.pytest.org/en/7.4.x/) as our test runner:

```sh
python -m pytest --pyargs calamancy
```

## 👩‍💻 Usage

To use calamanCy you first have to download either the medium, large, or
transformer model. To see a list of all available models, run:

```python
import calamancy
from model in calamancy.models():
    print(model)

# ..
# tl_calamancy_md-0.1.0
# tl_calamancy_lg-0.1.0
# tl_calamancy_trf-0.1.0
```

To download and load a model, run:

```python
nlp = calamancy.load("tl_calamancy_md-0.1.0")
doc = nlp("Ako si Juan de la Cruz")
```

The `nlp` object is an instance of spaCy's [`Language`
class](https://spacy.io/api/language) and you can use it as any other spaCy
pipeline. You can also [access these models on Hugging Face](https://huggingface.co/ljvmiranda921) 🤗.

## 📦 Models and Datasets

calamanCy provides Tagalog models and datasets that you can use in your spaCy
pipelines. You can download them directly or use the `calamancy` Python library
to access them. The training procedure for each pipeline can be found in the
`models/` directory. They are further subdivided into versions. Each folder is
an instance of a [spaCy project](https://spacy.io/usage/projects).

Here are the models for the latest release:

| Model                       | Pipelines                                   | Description                                                                                                  |
| --------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| tl_calamancy_md (73.7 MB)   | tok2vec, tagger, morphologizer, parser, ner | CPU-optimized Tagalog NLP model. Pretrained using the TLUnified dataset. Using floret vectors (50k keys)     |
| tl_calamancy_lg (431.9 MB)  | tok2vec, tagger, morphologizer, parser, ner | CPU-optimized large Tagalog NLP model. Pretrained using the TLUnified dataset. Using fastText vectors (714k) |
| tl_calamancy_trf (775.6 MB) | transformer, tagger, parser, ner            | GPU-optimized transformer Tagalog NLP model. Uses roberta-tagalog-base as context vectors.                   |

## 📓 API

The calamanCy library contains utility functions that help you load its models
and infer on your text. You can think of these functions as "syntactic sugar"
to the spaCy API. We highly recommend checking out the [spaCy Doc
object](https://spacy.io/api/doc), as it provides the most flexibility.

### Loaders

The loader functions provide an easier interface to download calamanCy models.
These models are hosted on [HuggingFace](https://huggingface.co/ljvmiranda921)
so you can try them out first before downloading.

#### <kbd>function</kbd> `get_latest_version`

Return the latest version of a calamanCy model.

| Argument    | Type  | Description                      |
| ----------- | ----- | -------------------------------- |
| `model`     | `str` | The string indicating the model. |
| **RETURNS** | `str` | The latest version of the model. |

#### <kbd>function</kbd> `models`

Get a list of valid calamanCy models.

| Argument    | Type        | Description                    |
| ----------- | ----------- | ------------------------------ |
| **RETURNS** | `List[str]` | List of valid calamanCy models |

#### <kbd>function</kbd> `load`

Load a calamanCy model as a [spaCy language pipeline](https://spacy.io/usage/processing-pipelines).

| Argument    | Type                                        | Description                                                                                  |
| ----------- | ------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `model`     | `str`                                       | The model to download. See the available models at [`calamancy.models()`](#function-models). |
| `force`     | `bool`                                      | Force download the model. Defaults to `False`.                                               |
| `**kwargs`  | `dict`                                      | Additional arguments to `spacy.load()`.                                                      |
| **RETURNS** | [`Language`](https://spacy.io/api/language) | A spaCy language pipeline.                                                                   |

### Inference

Below are lightweight utility classes for users who are not familiar with spaCy's
primitives. They are only useful for inference and not for training. If you wish
to train on top of these calamanCy models (e.g., text categorization,
task-specific NER, etc.), we advise you to follow the standard [spaCy training
workflow](https://spacy.io/usage/training).

General usage: first, you need to instantiate a class with the name of a model.
Then, you can use the `__call__` method to perform the prediction. The output
is of the type `Iterable[Tuple[str, Any]]` where the first part of the tuple
is the token and the second part is its label.

#### <kbd>method</kbd> `EntityRecognizer.__call__`

Perform named entity recognition (NER). By default, it uses the v0.1.0 of
[TLUnified-NER](https://huggingface.co/datasets/ljvmiranda921/tlunified-ner)
with the following entity labels: _PER (Person), ORG (Organization), LOC
(Location)._

| Argument   | Type                        | Description                             |
| ---------- | --------------------------- | --------------------------------------- |
| `text`     | `str`                       | The text to get the entities from.      |
| **YIELDS** | `Iterable[Tuple[str, str]]` | the token and its entity in IOB format. |

#### <kbd>method</kbd> `Tagger.__call__`

Perform parts-of-speech tagging. It uses the annotations from the
[TRG](https://universaldependencies.org/treebanks/tl_trg/index.html) and
[Ugnayan](https://universaldependencies.org/treebanks/tl_ugnayan/index.html)
treebanks with the following tags: _ADJ, ADP, ADV, AUX, DET, INTJ, NOUN, PART,
PRON, PROPN, PUNCT, SCONJ, VERB._

| Argument   | Type                                    | Description                                         |
| ---------- | --------------------------------------- | --------------------------------------------------- |
| `text`     | `str`                                   | The text to get the POS tags from.                  |
| **YIELDS** | `Iterable[Tuple[str, Tuple[str, str]]]` | the token and its coarse- and fine-grained POS tag. |

#### <kbd>method</kbd> `Parser.__call__`

Perform syntactic dependency parsing. It uses the annotations from the
[TRG](https://universaldependencies.org/treebanks/tl_trg/index.html) and
[Ugnayan](https://universaldependencies.org/treebanks/tl_ugnayan/index.html) treebanks.

| Argument   | Type                        | Description                                    |
| ---------- | --------------------------- | ---------------------------------------------- |
| `text`     | `str`                       | The text to get the dependency relations from. |
| **YIELDS** | `Iterable[Tuple[str, str]]` | the token and its dependency relation.         |

## 📝 Reporting Issues

If you have questions regarding the usage of `calamanCy`, bug reports, or just
want to give us feedback after giving it a spin, please use the [Issue
tracker](https://github.com/ljvmiranda921/calamancy/issues). Thank you!

## 📜 Citation

If you are citing the open-source software, please use:

```bib
@inproceedings{miranda-2023-calamancy,
    title = "calaman{C}y: A {T}agalog Natural Language Processing Toolkit",
    author = "Miranda, Lester James",
    editor = "Tan, Liling  and
      Milajevs, Dmitrijs  and
      Chauhan, Geeticka  and
      Gwinnup, Jeremy  and
      Rippeth, Elijah",
    booktitle = "Proceedings of the 3rd Workshop for Natural Language Processing Open Source Software (NLP-OSS 2023)",
    month = dec,
    year = "2023",
    address = "Singapore, Singapore",
    publisher = "Empirical Methods in Natural Language Processing",
    url = "https://aclanthology.org/2023.nlposs-1.1",
    pages = "1--7",
    abstract = "We introduce calamanCy, an open-source toolkit for constructing natural language processing (NLP) pipelines for Tagalog. It is built on top of spaCy, enabling easy experimentation and integration with other frameworks. calamanCy addresses the development gap by providing a consistent API for building NLP applications and offering general-purpose multitask models with out-of-the-box support for dependency parsing, parts-of-speech (POS) tagging, and named entity recognition (NER). calamanCy aims to accelerate the progress of Tagalog NLP by consolidating disjointed resources in a unified framework.The calamanCy toolkit is available on GitHub: https://github.com/ljvmiranda921/calamanCy.",
}
```

If you are citing the [NER dataset](https://huggingface.co/ljvmiranda921), please use:

```bib
@inproceedings{miranda-2023-developing,
    title = "Developing a Named Entity Recognition Dataset for {T}agalog",
    author = "Miranda, Lester James",
    editor = "Wijaya, Derry  and
      Aji, Alham Fikri  and
      Vania, Clara  and
      Winata, Genta Indra  and
      Purwarianti, Ayu",
    booktitle = "Proceedings of the First Workshop in South East Asian Language Processing",
    month = nov,
    year = "2023",
    address = "Nusa Dua, Bali, Indonesia",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.sealp-1.2",
    doi = "10.18653/v1/2023.sealp-1.2",
    pages = "13--20",
}
```
