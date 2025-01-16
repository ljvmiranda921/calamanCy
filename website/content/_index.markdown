---
title: Home
---

[<img src="https://raw.githubusercontent.com/ljvmiranda921/calamanCy/refs/heads/master/logo.png" style="max-width:15%;min-width:40px;float:right;" alt="Github repo" />](https://github.com/ljvmiranda921/calamanCy)

# calamanCy: NLP pipelines for Tagalog

**calamanCy** is a Tagalog natural language preprocessing framework made with [spaCy](https://spacy.io).
Its goal is to provide pipelines and datasets for core NLP tasks such as dependency parsing, morphological analysis, parts-of-speech tagging, and named entity recognition.
calamanCy takes inspiration from other language-specific spaCy frameworks such as [DaCy](https://github.com/centre-for-humanities-computing/DaCy) (Danish) and [huSpaCy](https://github.com/huspacy/huspacy) (Hungarian).

The name is based on _calamansi_, a citrus fruit native to the Philippines and used in traditional Filipino cuisine.

## Running your first pipeline

First install calamanCy, then download either the medium, large, or transformer model.
The command below automatically downloads and load the model you pass:

```python
!pip install calamanCy

nlp = calamancy.load("tl_calamancy_md-0.1.0")
doc = nlp("Ako si Juan de la Cruz")
```

You can see all available calamanCy models in this [🤗 HuggingFace collection](https://huggingface.co/collections/ljvmiranda921/calamancy-models-for-tagalog-nlp-65629cc46ef2a1d0f9605c87).
Alternatively, you can use all the calamanCy models within the spaCy library:

```python
!pip install spacy
!pip install https://huggingface.co/ljvmiranda921/tl_calamancy_md/resolve/main/tl_calamancy_md-any-py3-none-any.whl

import spacy
nlp = spacy.load("tl_calamancy_md")
doc = nlp("Ako si Juan de la Cruz")
```

To learn more about how calamanCy (or spaCy) process your text, feel free to explore the [official documentation](https://spacy.io/usage/processing-pipelines).

## Citation

If you're using calamanCy in your paper, please cite our publication:

```bibtex
@inproceedings{miranda-2023-calamancy,
    title = "calaman{C}y: A {T}agalog Natural Language Processing Toolkit",
    author = "Miranda, Lester James",
    booktitle = "Proceedings of the 3rd Workshop for Natural Language Processing Open Source Software (NLP-OSS 2023)",
    month = dec,
    year = "2023",
    address = "Singapore",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.nlposs-1.1/",
    doi = "10.18653/v1/2023.nlposs-1.1",
    pages = "1--7",
}
```

## Posts
