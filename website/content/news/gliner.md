---
title: New GliNER models for Tagalog NER
date: "2024-08-01"
---

I'm happy to share finetuned GliNER models for Tagalog NER!

[**GliNER**](https://github.com/urchade/GLiNER) (Generalist and Lightweight Model for Named Entity Recognition) is a powerful model capable of identifying any entity type using a BERT-like encoder.
This means that you don't need to train an NER model from scratch: just provide the entities you're interested in and you're all set!

These finetunes aren't really part of the core calamanCy line of models, but these GliNER-style models are really powerful so I took the opportunity to train some!

## The Tagalog GliNER models

I finetuned three models using GliNER v2.5 on top of [TLUnified-NER](https://huggingface.co/datasets/ljvmiranda921/tlunified-ner) for different size and compute requirements:
[`tl_gliner_small`](https://huggingface.co/ljvmiranda921/tl_gliner_small) (1.67 GB), [`tl_gliner_medium`](https://huggingface.co/ljvmiranda921/tl_gliner_medium) (1.99 GB), and [`tl_gliner_large`](https://huggingface.co/ljvmiranda921/tl_gliner_large) (3.68 GB).
You can replicate the finetuning process in this [directory](https://github.com/ljvmiranda921/calamanCy/tree/master/models/v0.1.0-gliner).

To use these GliNER models, you first need to install `gliner`:

```sh
pip install gliner==0.2.8 spacy gliner-spacy
```

Then, let's load the `tl_gliner_small` model:

```python
from gliner import GLiNER

# Initialize GLiNER with the base model
model = GLiNER.from_pretrained("ljvmiranda921/tl_gliner_small")
```

Let's define some _entities_ that we want to find in a given text.
Note that these entities were only seen during test-time, this means that GliNER models can detect entities in a zero-shot fashion!

```python
# Labels for entity prediction
# Most GLiNER models should work best when entity types are in lower case or title case
labels = ["person", "organization", "location"]

# Reference: Leni Robredo’s speech at the 2022 UP College of Law recognition rites
text = """
Nagsimula ako sa Public Attorney’s Office, kung saan araw-araw, mula Lunes hanggang Biyernes, nasa loob ako ng iba’t ibang court room at tambak ang kaso.
Bawat Sabado, nasa BJMP ako para ihanda ang aking mga kliyente. Nahasa ako sa crim law at litigation. Pero kinalaunan, lumipat ako sa isang NGO,
‘yung Sentro ng Alternatibong Lingap Panligal. Sa SALIGAN talaga ako nahubog bilang abugado: imbes na tinatanggap na lang ang mga batas na kailangang
sundin, nagtatanong din kung ito ba ay tunay na instrumento para makapagbigay ng katarungan sa ordinaryong Pilipino. Imbes na maghintay ng mga kliyente
sa de-aircon na opisina, dinadayo namin ang mga malalayong komunidad. Kadalasan, naka-tsinelas, naka-t-shirt at maong, hinahanap namin ang mga komunidad,
tinatawid ang mga bundok, palayan, at mga ilog para tumungo sa mga lugar kung saan hirap ang mga batayang sektor na makakuha ng access to justice.
Naaalala ko pa noong naging lead lawyer ako para sa isang proyekto: sa loob ng mahigit dalawang taon, bumibiyahe ako buwan-buwan papunta sa malayong
isla ng Masbate, nagpa-paralegal training sa mga batayang sektor doon, ipinapaliwanag, itinituturo, at sinasanay sila sa mga batas na nagbibigay-proteksyon
sa mga karapatan nila.
"""
```

To perform prediction, we do:

```python
# Display predicted entities and their labels
for entity in entities:
    print(entity["text"], "=>", entity["label"])

# Sample output:
# Public Attorney’s Office => organization
# BJMP => organization
# Sentro ng Alternatibong Lingap Panligal => organization
# Masbate => location
```

## Comparison against other Tagalog NER models

The evaluation results for TLUnified-NER are shown in the table below (reported numbers are F1-scores):

|                                                                                            | PER       | ORG       | LOC       | Overall   |
| ------------------------------------------------------------------------------------------ | --------- | --------- | --------- | --------- |
| [tl_gliner_small](https://huggingface.co/ljvmiranda921/tl_gliner_small)                    | 86.76     | 78.72     | 86.78     | 84.83     |
| [tl_gliner_medium](https://huggingface.co/ljvmiranda921/tl_gliner_medium)                  | 87.46     | 79.71     | 86.75     | 85.40     |
| [tl_gliner_large](https://huggingface.co/ljvmiranda921/tl_gliner_large)                    | 86.75     | 80.20     | 86.76     | 85.72     |
| [tl_calamancy_trf](https://huggingface.co/ljvmiranda921/tl_calamancy_trf)                  | 91.95     | **84.84** | 88.92     | 88.03     |
| [span-marker](https://huggingface.co/tomaarsen/span-marker-roberta-tagalog-base-tlunified) | **92.57** | 82.04     | **90.56** | **89.62** |

In general, **GliNER gets decent scores, but nothing beats regular finetuning on BERT-based models** as seen in [tl_calamancy_trf](https://huggingface.co/ljvmiranda921/tl_calamancy_trf) and [span_marker](https://huggingface.co/tomaarsen/span-marker-roberta-tagalog-base-tlunified).
The performance on Universal NER is generally worse (the highest is around ~50%), compared to the reported results in the Universal NER paper (we finetuned on RoBERTa as well).
One possible reason is that the annotation guidelines for TULunified-NER are more loose, because we consider some entities that Universal NER ignores.
At the same time, the text distribution of the two datasets are widely different.

Nevertheless, I'm still releasing these GliNER models as they are very extensible to other entity types (and it's also nice to have a finetuned version of GliNER for Tagalog!).
I **haven't done any extensive hyperparameter tuning** here so it might be nice if someone can contribute better config parameters to bump up these scores.
