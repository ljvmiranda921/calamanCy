from typing import Optional, Dict
from pathlib import Path

import typer
import spacy
from wasabi import msg
from datasets import load_dataset
from spacy.tokens import Doc, DocBin

# Reference: https://huggingface.co/datasets/wikiann#data-fields
WIKIANN_IOB = ["O", "B-PER", "I-PER", "B-ORG", "I-LOC", "B-LOC", "I-LOC"]


def download_datasets(
    # fmt: off
    wikitext_filename: str = typer.Option("wikitext", "--wikitext", help="Filename to save WikiText data.", show_default=True),
    wikiann_filename: str = typer.Option("wikiann", "--wikiann", help="Filename to save WikiANN data.", show_default=True),
    output_dir: Optional[Path] = typer.Option(None, "--output", "--output-dir", "-o", help="Output directory to save the spaCy datasets."),
    # fmt: on
):
    """Download the WikiText and WikiANN datasets from Huggingface and saves
    them in spaCy format"""
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
        save_to_disk(wikiann_spacy, wikiann_filename, output_dir)

    msg.info("Downloading and processing WikiText (tl) dataset")
    wikitext = load_dataset("wikitext_tl39")
    wikitext_spacy: Dict[str, DocBin]
    for split in wikitext.keys():
        docs = []
        data_dict = wikitext[split].to_dict()
        for text in data_dict["text"]:
            # Construct spaCy Doc
            doc = nlp(text)
            docs.append(doc)
        msg.text(f"Split `{split}` contains {len(docs)} documents.")
        wikitext_spacy[split] = DocBin(docs=docs)

    if output_dir:
        save_to_disk(wikitext_spacy, wikitext_filename, output_dir)


def save_to_disk(data_dict: Dict[str, DocBin], filename: str, output_dir: Path):
    for split, doc_bin in data_dict.items():
        output_path = output_dir / f"{filename}-{split}.spacy"
        output_path.mkdir(parents=True, exist_ok=True)
        doc_bin.to_disk(output_path)
        msg.good(f"Saved to {output_path}")


if __name__ == "__main__":
    typer.run(download_datasets)
