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
