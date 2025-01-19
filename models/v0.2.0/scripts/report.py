from pathlib import Path
from typing import Any

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
            model_name = model_dir.name
            for json_file in model_dir.glob("*.json"):
                task, dataset = json_file.stem.split("_")
                data = read_json(json_file)
                results.append((model_name, task, dataset, data))

    msg.info(f"Found {len(results)} results in {indir}")

    msg.text("Parsing syntactic annotation results...")
    syn_rows = []
    for result in results:
        pass

    msg.text("Parsing NER results...")
    ner_rows = []


def parse_syntactic_results(results: dict[str, Any]) -> dict[str, float]:
    """Get tokenizer, lemmatization, morph, and parsing evals"""
    pass


def parse_ner_results(results: dict[str, Any]) -> dict[str, float]:
    """Get NER evals"""
    pass


if __name__ == "__main__":
    typer.run(report)
