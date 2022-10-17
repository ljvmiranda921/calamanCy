from typing import Optional
from pathlib import Path

import typer
from wasabi import msg


def download_datasets(
    # fmt: off
    wikitext: str = typer.Option("wikitext", "--wikitext", help="Filename to save WikiText data.", show_default=True),
    wikiann: str = typer.Option("wikiann", "--wikiann", help="Filename to save WikiANN data.", show_default=True),
    output_dir: Optional[Path] = typer.Option(None, "--output", "--output-dir", "-o", help="Output directory to save the spaCy datasets."),
    # fmt: on
):
    """Download the WikiText and WikiANN datasets from Huggingface and saves
    them in spaCy format"""

    # Download datasets from Huggingface

    # Convert to spaCy DocBin

    # Save to disk
    if output_dir:
        pass


if __name__ == "__main__":
    typer.run(download_datasets)
