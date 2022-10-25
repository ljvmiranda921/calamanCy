from typing import List, Dict
import typer
import srsly
from pathlib import Path
from wasabi import msg


EXPERIMENT_TYPES = ["cross", "mono"]


def collate_results(
    # fmt: off
    metrics_dir: Path = typer.Argument(..., help="Path to the metrics directory"),
    dataset: str = typer.Argument(..., help="Name of the test dataset to evaluate with"),
    model: str = typer.Option("tl_tlunified_silver", "--model", "-M", help="Name of the model to summarize results"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Set verbosity")
    # fmt: on
):
    """Summarize results given a metrics folder"""
    for experiment in EXPERIMENT_TYPES:
        experiment_dir = metrics_dir / experiment / dataset
        if experiment_dir.is_dir():
            msg.divider(str(experiment_dir))
            results = _get_experiment_results(experiment_dir, model)
            breakpoint()


def _get_experiment_results(dir: Path, model: str) -> List[Dict]:
    json_files = [f for f in dir.glob("**/*") if str(f.name).startswith(model)]
    msg.info(f"Found {len(json_files)} trials for model '{model}'")

    results = []
    for f in json_files:
        results.append(srsly.read_json(f))
    return results


if __name__ == "__main__":
    typer.run(collate_results)
