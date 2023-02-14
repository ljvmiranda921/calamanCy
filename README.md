<img src="https://raw.githubusercontent.com/ljvmiranda921/calamanCy/master/logo.png" width="125" height="125" align="right" />

# calamanCy: NLP pipelines for Tagalog [WIP]

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

## 👩‍💻 Usage

To use the calamanCy you first have to download either the medium, large, or
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
```

This will download the model to the `.calamancy` directory of your home
directory. You can also download a model to a specific directory:

```python
calamancy.download_model("tl_calamancy_md-0.1.0", save_directory)
nlp = calamancy.load_model("tl_calamancy_md-0.1.0", save_directory)
```

The `nlp` object is an instance of spaCy's [`Language`
class](https://spacy.io/api/language), and you can use it as any other spaCy
pipeline. Head over to the [documentation]() for more tutorials.

## 📦 Models and Datasets

calamanCy provides Tagalog models and datasets that you can use in your spaCy
pipelines. You can download them directly or use the `calamancy` Python library
to access them.

### Datasets

You can find structured evaluation results for each dataset in the `datasets/` directory.


| Name                | Type | Task | Train | Dev | Test | Labels        | Description                                                       |
|---------------------|------|------|-------|-----|------|---------------|-------------------------------------------------------------------|
| `tl_tlunified_gold` | Gold | NER  | 6252  | 782 | 782  | PER, ORG, LOC | Annotated portion of the TLUnified corpus (Cruz and Cheng, 2021). |

### Pipelines

The training procedure for each pipeline can be found in the `training/` directory. They are further
subdivided into versions. Each folder is an instance of a [spaCy project](https://spacy.io/usage/projects).


| Name               | Components                                                    | Sources                                             | Description                                                                                                                                                                                    |
|--------------------|---------------------------------------------------------------|-----------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `tl_calamancy_md`  | tok2vec, morphologizer, parser, trainable_lemmatizer, ner     | TLUnified (Cruz and Cheng, 2021), UD Tagalog (2023) | Floret vectors (200k) that were trained from the bulk of TLUnified were used for the tok2vec component. Similar to the `lg` variant, it also uses character pretraining to initialize weights. |
| `tl_calamancy_lg`  | tok2vec, morphologizer, parser, trainable_lemmatizer, ner     | TLUnified (Cruz and Cheng, 2021), UD Tagalog (2023) | The tok2vec component uses fastText vectors (714k) trained from CommonCrawl and Wikipedia. It also uses character pretraining to initialize the token-to-vector weights.                       |
| `tl_calamancy_trf` | transformer, morphologizer, parser, trainable_lemmatizer, ner | TLUnified (Cruz and Cheng, 2021), UD Tagalog (2023) | The transformer component uses roberta-tagalog-large.                                                                                                                                          |

