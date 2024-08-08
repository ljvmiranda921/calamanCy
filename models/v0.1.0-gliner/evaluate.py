from pathlib import Path
from typing import Optional, Dict, List

import torch
import typer
import spacy
from wasabi import msg
from spacy.tokens import Doc
from datasets import load_dataset, Dataset


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
    ds = load_dataset(dataset, dataset_config, split="test")
    gold_docs = convert_to_spacy_docs(ds)

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
    pred_docs = nlp(docs)


def process_labels(label_map: str) -> Dict[str, str]:
    return {m.split("::")[0]: m.split("::")[1] for m in label_map.split(",")}


def convert_to_spacy_docs(ds: "Dataset") -> List[Doc]:
    pass


if __name__ == "__main__":
    typer.run(main)
