from pathlib import Path

import typer
import pandas as pd
from srsly import read_json
from wasabi import msg


def report(
    indir: Path = typer.Argument(..., help="Path to the evaluations directory.")
):
    """Return a table of evaluation results

    The input to `indir` must be a directory where the first-level directories are the model names,
    with JSON files from `spacy evaluate` in this file format: {task}_{dataset}.json
    """
    results = []
    for model_dir in indir.iterdir():
        if model_dir.is_dir():
            for json_file in model_dir.glob("*.json"):
                data = read_json(json_file)
                results.append(data)
    breakpoint()


if __name__ == "__main__":
    typer.run(report)
