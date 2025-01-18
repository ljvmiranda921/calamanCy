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
