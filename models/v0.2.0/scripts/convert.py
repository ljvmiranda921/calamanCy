from pathlib import Path
from typing import Optional

import typer
from spacy.tokens import Doc, DocBin
from wasabi import msg


def convert(
    # fmt: off
    infile: Path = typer.Argument(..., help="Path to input file to convert."),
    outfile: Path = typer.Argument(..., help="Path to save the converted DocBin in .spacy format."),
    converter: Optional[str] = typer.Option(None, help="Converter to use")
    # fmt: on
):
    pass
