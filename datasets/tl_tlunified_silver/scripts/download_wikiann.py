from typing import Optional, Dict
from pathlib import Path

import typer
import spacy
from wasabi import msg
from datasets import load_dataset
from spacy.tokens import Doc, DocBin

# Reference: https://huggingface.co/datasets/wikiann#data-fields
WIKIANN_IOB = ["O", "B-PER", "I-PER", "B-ORG", "I-LOC", "B-LOC", "I-LOC"]


def download_wikiann(
    # fmt: off
    filename: str = typer.Option("wikiann", "--filename", "-f", help="Filename to save WikiANN data.", show_default=True),
    output_dir: Optional[Path] = typer.Option(None, "--output", "--output-dir", "-o", help="Output directory to save the spaCy datasets."),
    # fmt: on
):
    """Download the WikiANN dataset from Huggingface and save it in spaCy format"""
    nlp = spacy.blank("tl")

    msg.info("Downloading and processing WikiANN (tl) dataset")
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
        msg.text(f"Split `{split}` contains {len(docs)} documents.")
        wikiann_spacy[split] = DocBin(docs=docs, attrs=["ENT_IOB", "ENT_TYPE"])

    if output_dir:
        for split, doc_bin in wikiann_spacy.items():
            output_path = output_dir / f"{filename}-{split}.spacy"
            output_path.mkdir(parents=True, exist_ok=True)
            doc_bin.to_disk(output_path)
            msg.good(f"Saved to {output_path}")


if __name__ == "__main__":
    typer.run(download_wikiann)
