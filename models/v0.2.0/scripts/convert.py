from pathlib import Path
from typing import Optional

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
        # TODO: Get texts and labels
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

        converter = convert_ner
    elif source == "tfnerd":
        # TODO: Get texts and labels
        texts = []
        labels = []
        converter = convert_ner
    else:
        msg.fail(f"Unknown source: {source}", exits=1)

    # Perform conversion to DocBin
    docs = convert_ner(texts, labels)
    # Save to outfile


def convert_ner(texts: list[list[str]], labels: list[list[str]]) -> list[Doc]:
    pass


if __name__ == "__main__":
    typer.run(convert)
