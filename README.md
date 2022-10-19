# CalamanCy [WIP]

**CalamanCy** is a Tagalog natural language preprocessing framework made with [spaCy](https://spacy.io).
Its goal is to provide silver-standard pipelines and datasets for downstream NLP
tasks. This repository contains material for using CalamanCy, reproduction of
results, and guides on usage. 

> CalamanCy takes inspiration from other language-specific [spaCy Universe frameworks](https://spacy.io/universe) such as 
> [DaCy](https://github.com/centre-for-humanities-computing/DaCy), [huSpaCy](https://github.com/huspacy/huspacy),
> and [graCy](https://github.com/jmyerston/graCy). The name is based from [*calamansi*](https://en.wikipedia.org/wiki/Calamansi),
> a citrus fruit native to the Philippines and used in traditional Filipino cuisine.

## 🔧 Installation

To get started with CalamanCy, simply install it using `pip` by running the
following line in your terminal:

```sh
pip install calamancy
``` 

## 👩‍💻 Usage

To use the models you first have to download either the small, medium, or large model. To see a list 
of all available models, run:

```python
import calamancy
from model in calamancy.models():
    print(model)

# ..
# tl_calamancy_sm-0.1.0
# tl_calamancy_md-0.1.0
# tl_calamancy_lg-0.1.0
```

To download and load a model, run:

```python
nlp = calamancy.load("tl_calamancy_sm-0.1.0")
```

This will download the model to the `.calamancy` directory of your home
directory. You can also download a model to a specific directory:

```python
calamancy.download_model("tl_calamancy_sm-0.1.0", save_directory)
nlp = calamancy.load_model("tl_calamancy_sm-0.1.0", save_directory)
```

The `nlp` object is an instance of spaCy's [`Language`
class](https://spacy.io/api/language), and you can use it as any other spaCy
pipeline. Head over to the [documentation]() for more tutorials.

## 📦 Models and Datasets

CalamanCy provides Tagalog models and datasets that you can use in your spaCy
pipelines.  As a low-resource language, most of these are based on
**silver-standard** data. You can check the `training/` and `datasets/`
directories to verify and reproduce these outputs (each folder is an instance of
a [spaCy project](https://spacy.io/usage/projects)).

### Datasets

| Name                | Type                  | Description                                                                                                           |
|---------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------|
| [`tl_calamancy_silver`](https://github.com/ljvmiranda921/calamanCy/tree/master/datasets/tl_calamancy_silver_corpus) | Silver-standard (NER) | Silver-standard dataset based from the [TLUnified corpus](https://arxiv.org/abs/2111.06053) by Cruz and Cheng (2022). |

### Pipelines

| Name                             | Pipeline Components   | Description                                                          |
|----------------------------------|--------------|----------------------------------------------------------------------|
| [`tl_calamancy_silver_{sm,md,lg}`]() | tok2vec, ner        | Model trained from the silver-standard `tl_calamancy_silver` corpus. Variants: [`sm`]() (XX vectors), [`md`]() (XX vectors), [`lg`]() XX vectors) |
| [`tl_calamancy_silver_trf`]() | transformer, ner        | Transformer-based model trained from the silver-standard [`tl_calamancy_silver`]() corpus. |
