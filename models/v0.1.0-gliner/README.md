<!-- WEASEL: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 Weasel Project: Release v0.1.0-gliner

This is a spaCy project that trains and evaluates new v0.1.0-gliner models.
[GliNER](https://github.com/urchade/GLiNER) (Generalist and Lightweight Model for Named Entity Recognition) is a powerful model capable of identifying any entity type using a BERT-like encoder.
In this project, we finetune the GliNER model with the TLUnified-NER training dataset.

To replicate training, first you need to install the required dependencies:

```
pip install -r requirements.txt
```

## Training

To train a GliNER model, run the `finetune-*` workflow like so:

```
python -m spacy project run finetune-gliner-sm
python -m spacy project run finetune-gliner-md
python -m spacy project run finetune-gliner-lg
# train all at once
python -m spacy project run finetune-all
```

The models are currently [based on the v2.5 version of GliNER](https://huggingface.co/collections/urchade/gliner-v25-66743e64ab975c859119d1eb).

## Evaluation

To perform evals, run the `eval-*` workflows:

```
python -m spacy project run eval-gliner-sm
python -m spacy project run eval-gliner-md
python -m spacy project run eval-gliner-lg
```

This will evaluate on TLUnified-NER's test set ([Miranda, 2023](https://aclanthology.org/2023.sealp-1.2.pdf) and the Tagalog subsets of
Universal NER ([Mayhew et al., 2024](https://aclanthology.org/2024.naacl-long.243/)).


## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[Weasel documentation](https://github.com/explosion/weasel).

<!-- WEASEL: AUTO-GENERATED DOCS END (do not remove) -->