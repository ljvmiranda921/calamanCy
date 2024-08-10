<!-- WEASEL: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 Weasel Project: Release v0.1.0-gliner

This is a spaCy project that trains and evaluates new v0.1.0-gliner models.
[GliNER](https://github.com/urchade/GLiNER) (Generalist and Lightweight Model for Named Entity Recognition) is a powerful model capable of identifying any entity type using a BERT-like encoder.
In this project, we finetune the GliNER model using the TLUnified-NER dataset.

To replicate training, first you need to install the required dependencies:

```sh
pip install -r requirements.txt
```

## Training

To train a GliNER model, run the `finetune-gliner` workflow while passing the size:

```sh
# Available options: 'small', 'medium', 'large'
python -m spacy project run finetune-gliner . --vars.size small
```

The models are currently based on the [v2.5 version of GliNER](https://huggingface.co/collections/urchade/gliner-v25-66743e64ab975c859119d1eb).

## Evaluation

To perform evals, run the `eval-gliner` workflow while passing the size:

```sh
# Available options: 'small', 'medium', 'large'
python -m spacy project run eval-gliner . --vars.size small
```

This will evaluate on TLUnified-NER's test set ([Miranda, 2023](https://aclanthology.org/2023.sealp-1.2.pdf)) and the Tagalog subsets of
Universal NER ([Mayhew et al., 2024](https://aclanthology.org/2024.naacl-long.243/)).

The evaluation results for TLUnified-NER are shown in the table below (reported numbers are F1-scores):

|                  | PER   | ORG   | LOC   | Overall |
|------------------|-------|-------|-------|---------|
| [tl_gliner_small](https://huggingface.co/ljvmiranda921/tl_gliner_small)  | 86.76 | 78.72 | 86.78 | 84.83   |
| [tl_gliner_medium](https://huggingface.co/ljvmiranda921/tl_gliner_medium) | 87.46 | 79.71 | 86.75 | 85.40   |
| [tl_gliner_large](https://huggingface.co/ljvmiranda921/tl_gliner_large)  | 86.75 | 80.20 | 86.76 | 85.72   |
| [tl_calamancy_trf](https://huggingface.co/ljvmiranda921/tl_calamancy_trf) | 91.95 | **84.84** | 88.92 | 88.03   |
| [span-marker](https://huggingface.co/tomaarsen/span-marker-roberta-tagalog-base-tlunified)      | **92.57** | 82.04 | **90.56** | **89.62**   |

In general, GliNER gets decent scores, but nothing beats regular finetuning on BERT-based models as seen in [tl_calamancy_trf](https://huggingface.co/ljvmiranda921/tl_calamancy_trf) and [span_marker](https://huggingface.co/tomaarsen/span-marker-roberta-tagalog-base-tlunified).
The performance on Universal NER is generally worse (the highest is around ~50%), compared to the reported results in the Universal NER paper (we finetuned on RoBERTa as well).
One possible reason is that the annotation guidelines for TULunified-NER are more loose, because we consider some entities that Universal NER ignores.
At the same time, the text distribution of the two datasets are widely different.

Nevertheless, I'm still releasing these GliNER models as they are very extensible to other entity types (and it's also nice to have a finetuned version of GliNER for Tagalog!).
I haven't done any extensive hyperparameter tuning here so it might be nice if someone can contribute better config parameters to bump up these scores.

## Usage

Here's how you can use the trained Tagalog GLiNER models:

```python
from gliner import GLiNER

# Initialize GLiNER with the base model
model = GLiNER.from_pretrained("ljvmiranda921/tl_gliner_small")

# Sample text for entity prediction
# Reference: Leni Robredo’s speech at the 2022 UP College of Law recognition rites
text = """"
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

# Labels for entity prediction
# Most GLiNER models should work best when entity types are in lower case or title case
labels = ["person", "organization", "location"]

# Perform entity prediction
entities = model.predict_entities(text, labels, threshold=0.5)

# Display predicted entities and their labels
for entity in entities:
    print(entity["text"], "=>", entity["label"])

# Sample output:
# Public Attorney’s Office => organization
# BJMP => organization
# Sentro ng Alternatibong Lingap Panligal => organization
# Masbate => location
```

## Citation

Please cite the following papers when using these models:

```bib
@misc{zaratiana2023gliner,
    title={GLiNER: Generalist Model for Named Entity Recognition using Bidirectional Transformer}, 
    author={Urchade Zaratiana and Nadi Tomeh and Pierre Holat and Thierry Charnois},
    year={2023},
    eprint={2311.08526},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```

```bib
@inproceedings{miranda-2023-calamancy,
  title = "calaman{C}y: A {T}agalog Natural Language Processing Toolkit",
  author = "Miranda, Lester James",
  booktitle = "Proceedings of the 3rd Workshop for Natural Language Processing Open Source Software (NLP-OSS 2023)",
  month = dec,
  year = "2023",
  address = "Singapore, Singapore",
  publisher = "Empirical Methods in Natural Language Processing",
  url = "https://aclanthology.org/2023.nlposs-1.1",
  pages = "1--7",
} 
```

If you're using the NER dataset:

```bib
@inproceedings{miranda-2023-developing,
  title = "Developing a Named Entity Recognition Dataset for {T}agalog",
  author = "Miranda, Lester James",
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
| `finetune-gliner` | Finetune the GliNER model using TLUnified-NER |
| `eval-gliner` | Evaluate trained GliNER models on the TLUnified-NER and Universal NER test sets |

<!-- WEASEL: AUTO-GENERATED DOCS END (do not remove) -->
