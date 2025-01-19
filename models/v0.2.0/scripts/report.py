from pathlib import Path

import typer
import pandas as pd
from srsly import read_jsonl
from wasabi import msg


def report(
    # fmt: off
    indir: Path = typer.Argument(..., help="")
    # fmt: on
):
    """Return a table of evaluation results

    The input to `indir` must be a directory where the first-level directories are the model names,
    with JSON files from `spacy evaluate` in this file format: {task}_{dataset}.json
    """
    pass


if __name__ == "__main__":
    typer.run(report)
