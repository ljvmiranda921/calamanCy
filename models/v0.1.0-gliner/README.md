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

The evaluation results are shown in the table below:

In general, GliNER is competitive with the current calamanCy models on TLUnified-NER, but it doesn't perform really well on Universal NER.
One possible reason is that the annotation guidelines for TULunified-NER are more loose, because we consider some entities that Universal NER ignores.
At the same time, the text distribution of the two datasets are widely different.

Nevertheless, I'm still releasing these GliNER models as they are very extensible to other entity types (and it's also nice to have a finetuned version of GliNER for Tagalog!).


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