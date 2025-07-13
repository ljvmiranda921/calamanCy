from pathlib import Path
from typing import Dict, Optional

import spacy
import typer
from datasets import load_dataset
from spacy.tokens import Doc, DocBin
from wasabi import msg

from .utils import setup_gpu

# Reference: https://huggingface.co/datasets/wikiann#data-fields
WIKIANN_IOB = ["O", "B-PER", "I-PER", "B-ORG", "I-LOC", "B-LOC", "I-LOC"]


def download_wikiann(
    # fmt: off
    filename: str = typer.Option("wikiann", "--filename", "-f", help="Filename to save WikiANN data.", show_default=True),
    output_dir: Optional[Path] = typer.Option(None, "--output", "--output-dir", "-o", help="Output directory to save the spaCy datasets."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Print extra output to console."),
    gpu_id: int = typer.Option(-1, "--gpu", "--gpu-id", "-g", help="Set the GPU ID.", show_default=True)
    # fmt: on
):
    """Download the WikiANN dataset from Huggingface and save it in spaCy format"""
    msg.info("Downloading and processing WikiANN (tl) dataset")
    setup_gpu(gpu_id, silent=verbose)
    nlp = spacy.blank("tl")
    wikiann = load_dataset("wikiann", "tl")
    wikiann_spacy: Dict[str, DocBin] = {}
    for split in wikiann.keys():
        docs = []
        data_dict = wikiann[split].to_dict()
        for tokens, ner_tags in zip(data_dict["tokens"], data_dict["ner_tags"]):
            # Construct spaCy Doc
            doc = Doc(
                nlp.vocab,
                words=tokens,
                ents=[WIKIANN_IOB[tag] for tag in ner_tags],
            )
            docs.append(doc)
        msg.text(f"Split {split} has {len(docs)} documents", show=verbose)
        wikiann_spacy[split] = DocBin(docs=docs, attrs=["ENT_IOB", "ENT_TYPE"])

    if output_dir:
        for split, doc_bin in wikiann_spacy.items():
            output_path = output_dir / f"{filename}-{split}.spacy"
            output_dir.mkdir(parents=True, exist_ok=True)
            doc_bin.to_disk(output_path)
            msg.good(f"Saved to {output_path} ({len(doc_bin)} documents)")


if __name__ == "__main__":
    typer.run(download_wikiann)
