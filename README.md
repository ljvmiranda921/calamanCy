<img src="https://raw.githubusercontent.com/ljvmiranda921/calamanCy/master/logo.png" width="125" height="125" align="right" />

# calamanCy: NLP pipelines for Tagalog

![example workflow](https://github.com/ljvmiranda921/calamancy/actions/workflows/test.yml/badge.svg)
![PyPI](https://img.shields.io/pypi/v/calamancy?labelColor=%23272c32&color=%2333cc56&logo=pypi&logoColor=white)



**calamanCy** is a Tagalog natural language preprocessing framework made with
[spaCy](https://spacy.io). Its goal is to provide pipelines and datasets for
downstream NLP tasks. This repository contains material for using calamanCy,
reproduction of results, and guides on usage. 

> calamanCy takes inspiration from other language-specific [spaCy Universe frameworks](https://spacy.io/universe) such as 
> [DaCy](https://github.com/centre-for-humanities-computing/DaCy), [huSpaCy](https://github.com/huspacy/huspacy),
> and [graCy](https://github.com/jmyerston/graCy). The name is based from [*calamansi*](https://en.wikipedia.org/wiki/Calamansi),
> a citrus fruit native to the Philippines and used in traditional Filipino cuisine.

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
|-----------------------------|---------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| tl_calamancy_md (73.7 MB)   | tok2vec, tagger, morphologizer, parser, ner | CPU-optimized Tagalog NLP model. Pretrained using the TLUnified dataset. Using floret vectors (50k keys)     |
| tl_calamancy_lg (431.9 MB)  | tok2vec, tagger, morphologizer, parser, ner | CPU-optimized large Tagalog NLP model. Pretrained using the TLUnified dataset. Using fastText vectors (714k) |
| tl_calamancy_trf (775.6 MB) | transformer, tagger, parser, ner            | GPU-optimized transformer Tagalog NLP model. Uses roberta-tagalog-base as context vectors.                   |

## 📓 API

The calamanCy library contains utility functions that help you load its models
and infer on your text.  You can think of these functions as "syntactic sugar"
to the spaCy API. We highly recommend checking out the [spaCy Doc
object](https://spacy.io/api/doc), as it provides the most flexibility.

### Loaders

The loader functions provide an easier interface to download calamanCy models.
These models are hosted on [HuggingFace](https://huggingface.co/ljvmiranda921)
so you can try them out first before downloading.

#### <kbd>function</kbd> `get_latest_version`

Return the latest version of a calamanCy model.

| Argument    | Type  | Description            |
| ----------- | ----- | ---------------------- |
| `model`     | `str` | The string indicating the model.   |
| **RETURNS** | `str` | The latest version of the model.   |


#### <kbd>function</kbd> `models`

Get a list of valid calamanCy models.

| Argument    | Type  | Description            |
| ----------- | ----- | ---------------------- |
| **RETURNS** | `List[str]` | List of valid calamanCy models   |


#### <kbd>function</kbd> `load`

Load a calamanCy model as a [spaCy language pipeline](https://spacy.io/usage/processing-pipelines).

| Argument    | Type  | Description            |
| ----------- | ----- | ---------------------- |
| `model`     | `str` | The model to download. See the available models at [`calamancy.models()`](#function-models).   |
| `force`     | `bool` | Force download the model. Defaults to `False`.   |
| `**kwargs`     | `dict` | Additional arguments to `spacy.load()`.   |
| **RETURNS** | [`Language`](https://spacy.io/api/language) | A spaCy language pipeline.   |


### Inference

Below are lightweight utility classes for users who are not familiar with spaCy's
primitives. They are only useful for inference and not for training. If you wish
to train on top of these calamanCy models (e.g., text categorization,
task-specific NER, etc.), we advice you to follow the standard [spaCy training
workflow](https://spacy.io/usage/training).

General usage: first, you need to instantiate a class with the name of a model.
Then, you can use the `__call__` method to perform the prediction. The output
is of the type `Iterable[Tuple[str, Any]]` where the first part of the tuple
is the token and the second part is its label.

#### <kbd>method</kbd> `EntityRecognizer.__call__`

Perform named entity recognition (NER).  By default, it uses the v0.1.0 of
[TLUnified-NER](https://huggingface.co/datasets/ljvmiranda921/tlunified-ner)
with the following entity labels: *PER (Person), ORG (Organization), LOC
(Location).*


| Argument    | Type  | Description            |
| ----------- | ----- | ---------------------- |
| `text`     | `str` | The text to get the entities from.   |
| **YIELDS** | `Iterable[Tuple[str, str]]` | the token and its entity in IOB format.   |

#### <kbd>method</kbd> `Tagger.__call__`

Perform parts-of-speech tagging. It uses the annotations from the
[TRG](https://universaldependencies.org/treebanks/tl_trg/index.html) and
[Ugnayan](https://universaldependencies.org/treebanks/tl_ugnayan/index.html)
treebanks with the following tags: *ADJ, ADP, ADV, AUX, DET, INTJ, NOUN, PART,
PRON, PROPN, PUNCT, SCONJ, VERB.*


| Argument    | Type  | Description            |
| ----------- | ----- | ---------------------- |
| `text`     | `str` | The text to get the POS tags from.   |
| **YIELDS** | `Iterable[Tuple[str, Tuple[str, str]]]` | the token and its coarse- and fine-grained POS tag.   |

#### <kbd>method</kbd> `Parser.__call__`

Perform syntactic dependency parsing. It uses the annotations from the
[TRG](https://universaldependencies.org/treebanks/tl_trg/index.html) and
[Ugnayan](https://universaldependencies.org/treebanks/tl_ugnayan/index.html) treebanks.


| Argument    | Type  | Description            |
| ----------- | ----- | ---------------------- |
| `text`     | `str` | The text to get the dependency relations from.   |
| **YIELDS** | `Iterable[Tuple[str, str]]` | the token and its dependency relation.   |


## 📝️ Reporting Issues

If you have questions regarding the usage of `calamanCy`, bug reports, or just
want to give us feedback after giving it a spin, please use the [Issue
tracker](https://github.com/ljvmiranda921/calamancy/issues). Thank you!