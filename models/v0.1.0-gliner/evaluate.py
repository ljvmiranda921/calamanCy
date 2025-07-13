from copy import deepcopy
from pathlib import Path
from typing import Dict, Iterable, Optional

import spacy
import srsly
import torch
import typer
from datasets import Dataset, load_dataset
from spacy.scorer import Scorer
from spacy.tokens import Doc, Span
from spacy.training import Example
from wasabi import msg


def main(
    # fmt: off
    output_path: Path = typer.Argument(..., help="Path to store the metrics in JSON format."),
    model_name: str = typer.Option("ljvmiranda921/tl_gliner_small", show_default=True, help="GliNER model to use for evaluation."),
    dataset: str = typer.Option("ljvmiranda921/tlunified-ner", help="Dataset to evaluate upon."),
    threshold: float = typer.Option(0.5, help="The threshold of the GliNER model (controls the degree to which a hit is considered an entity)."),
    dataset_config: Optional[str] = typer.Option(None, help="Configuration for loading the dataset."),
    chunk_size: int = typer.Option(250, help="Size of the text chunk to be processed at once."),
    label_map: str = typer.Option("person::PER,organization::ORG,location::LOC", help="Mapping between GliNER labels and the dataset's actual labels (separated by a double-colon '::')."),
    # fmt: on
):
    label_map: Dict[str, str] = process_labels(label_map)
    msg.text(f"Using label map: {label_map}")

    msg.info("Processing test dataset")
    ds = load_dataset(dataset, dataset_config, split="test", trust_remote_code=True)
    ref_docs = convert_hf_to_spacy_docs(ds)

    msg.info("Loading GliNER model")
    nlp = spacy.blank("tl")
    nlp.add_pipe(
        "gliner_spacy",
        config={
            "gliner_model": model_name,
            "chunk_size": chunk_size,
            "labels": list(label_map.keys()),
            "threshold": threshold,
            "style": "ent",
            "map_location": "cuda" if torch.cuda.is_available() else "cpu",
        },
    )
    msg.text("Getting predictions")
    docs = deepcopy(ref_docs)
    pred_docs = list(nlp.pipe(docs))
    pred_docs = [update_entity_labels(doc, label_map) for doc in pred_docs]

    # Get the scores
    examples = [
        Example(reference=ref, predicted=pred) for ref, pred in zip(ref_docs, pred_docs)
    ]
    scores = Scorer.score_spans(examples, "ents")

    msg.info(f"Results for {dataset} ({model_name})")
    msg.text(scores)
    srsly.write_json(output_path, data=scores, indent=2)
    msg.good(f"Saving outputs to {output_path}")


def process_labels(label_map: str) -> Dict[str, str]:
    return {m.split("::")[0]: m.split("::")[1] for m in label_map.split(",")}


def convert_hf_to_spacy_docs(dataset: "Dataset") -> Iterable[Doc]:
    nlp = spacy.blank("tl")
    examples = dataset.to_list()
    entity_types = {
        idx: feature.split("-")[1]
        for idx, feature in enumerate(dataset.features["ner_tags"].feature.names)
        if feature != "O"  # don't include empty
    }
    msg.text(f"Using entity types: {entity_types}")

    docs = []
    for example in examples:
        tokens = example["tokens"]
        ner_tags = example["ner_tags"]
        doc = Doc(nlp.vocab, words=tokens)

        entities = []
        start_idx = None
        entity_type = None

        for idx, tag in enumerate(ner_tags):
            if tag in entity_types:
                if start_idx is None:
                    start_idx = idx
                    entity_type = entity_types[tag]
                elif entity_type != entity_types.get(tag, None):
                    entities.append(Span(doc, start_idx, idx, label=entity_type))
                    start_idx = idx
                    entity_type = entity_types[tag]
            else:
                if start_idx is not None:
                    entities.append(Span(doc, start_idx, idx, label=entity_type))
                    start_idx = None

        if start_idx is not None:
            entities.append(Span(doc, start_idx, len(tokens), label=entity_type))
        doc.ents = entities
        docs.append(doc)

    return docs


def update_entity_labels(doc: Doc, label_mapping: Dict[str, str]) -> Doc:
    updated_ents = []
    for ent in doc.ents:
        new_label = label_mapping.get(ent.label_.lower(), ent.label_)
        updated_span = Span(doc, ent.start, ent.end, label=new_label)
        updated_ents.append(updated_span)

    new_doc = Doc(
        doc.vocab,
        words=[token.text for token in doc],
        spaces=[token.whitespace_ for token in doc],
    )
    new_doc.ents = updated_ents
    return new_doc


if __name__ == "__main__":
    typer.run(main)
