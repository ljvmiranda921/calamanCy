from pathlib import Path
from typing import Optional

import spacy
import typer
from spacy.tokens import Doc, DocBin, Span
from wasabi import msg


def convert(
    # fmt: off
    infile: Path = typer.Argument(..., help="Path to input file to convert."),
    outfile: Path = typer.Argument(..., help="Path to save the converted DocBin in .spacy format."),
    source: Optional[str] = typer.Option(None, "--source", help="Source of the dataset in order to determine how it will be converted.")
    # fmt: on
):
    if source == "uner":
        texts = []
        labels = []

        with infile.open("r", encoding="utf-8") as file:
            current_text = []
            current_labels = []
            for line in file:
                line = line.strip()
                if line.startswith("# text ="):
                    if current_text:
                        texts.append(current_text)
                        labels.append(current_labels)
                        current_text = []
                        current_labels = []
                elif line and not line.startswith("#"):
                    parts = line.split("\t")
                    if len(parts) >= 2:
                        word, label = parts[1], parts[2]
                        current_text.append(word)
                        current_labels.append(label)
            if current_text:
                texts.append(current_text)
                labels.append(current_labels)

    if source == "tfnerd":
        texts = []
        labels = []

        with infile.open("r", encoding="utf-8") as file:
            current_text = []
            current_labels = []
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(" ")
                    if len(parts) >= 2:
                        word, label = parts[0], parts[1].upper()
                        if label == "B-PERSON" or label == "I-PERSON":
                            label = label.replace("PERSON", "PER")
                        elif label == "B-ORGANIZATION" or label == "I-ORGANIZATION":
                            label = label.replace("ORGANIZATION", "ORG")
                        elif label == "B-LOCATION" or label == "I-LOCATION":
                            label = label.replace("LOCATION", "LOC")
                        current_text.append(word)
                        current_labels.append(label)
            if current_text:
                texts.append(current_text)
                labels.append(current_labels)
    else:
        msg.fail(f"Unknown source: {source}", exits=1)

    # Perform conversion to DocBin
    msg.info(f"Converting texts from {infile} to spaCy Doc objects")
    docs = [make_doc(tokens, label) for tokens, label in zip(texts, labels)]
    breakpoint()

    # Save docbin to outfile
    doc_bin = DocBin(docs=docs)
    doc_bin.to_disk(outfile)
    msg.good(f"Saved {len(docs)} documents to {outfile}!")


def make_doc(
    tokens: list[str],
    labels: list[str],
    allow_labels=["PER", "ORG", "LOC"],
) -> Doc:
    nlp = spacy.blank("tl")
    doc = Doc(nlp.vocab, words=tokens)
    ents = []
    start = None
    entity = None

    for i, (token, label) in enumerate(zip(tokens, labels)):
        if label.startswith("B-"):
            if start is not None:
                ents.append((start, i, entity))
            start = i
            entity = label[2:]
        elif label.startswith("I-") and start is not None and entity == label[2:]:
            continue
        else:
            if start is not None:
                ents.append((start, i, entity))
                start = None
                entity = None

    if start is not None:
        ents.append((start, len(tokens), entity))

    doc.ents = [
        Span(doc, start, end, label=entity)
        for start, end, entity in ents
        if entity in allow_labels
    ]
    return doc


if __name__ == "__main__":
    typer.run(convert)
