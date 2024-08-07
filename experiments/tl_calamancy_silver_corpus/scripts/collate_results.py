import statistics
from pathlib import Path
from typing import Any, Dict, List, Tuple

import srsly
import typer
from wasabi import msg

EXPERIMENT_TYPES = ["cross", "mono"]


def collate_results(
    # fmt: off
    metrics_dir: Path = typer.Argument(..., help="Path to the metrics directory"),
    dataset: str = typer.Argument(..., help="Name of the test dataset to evaluate with"),
    model: str = typer.Option("tl_tlunified_silver", "--model", "-M", help="Name of the model to summarize results"),
    per_entity_type: bool = typer.Option(False, "--per-entity-type", "-E", help="Show results per entity type"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Set verbosity")
    # fmt: on
):
    """Summarize results given a metrics folder"""
    for experiment in EXPERIMENT_TYPES:
        experiment_dir = metrics_dir / experiment / dataset
        if experiment_dir.is_dir():
            msg.divider(str(experiment_dir))
            results = _get_raw_results(experiment_dir, model)
            summary_metrics = _summarize_results(results, False)
            _format_table(summary_metrics)
            if per_entity_type:
                per_entity_metrics = _summarize_results(results, True)
                _format_entity_table(per_entity_metrics)


def _format_table(results: Dict[str, Any]) -> str:
    header = list(results.keys())
    data = [f"{mean:.2f} ({stdev:.2f})" for mean, stdev in list(results.values())]
    table = msg.table([data], header=header, divider=True)
    return table


def _format_entity_table(results: Dict[str, Dict[str, Tuple[float, float]]]) -> str:
    entities = list(results.keys())
    header = ["ents"] + list(results.get(entities[0]).keys())
    data = []
    for entity in entities:
        str_scores = [
            f"{mean:.2f} ({stdev:.2f})"
            for mean, stdev in list(results[entity].values())
        ]
        row = [entity] + str_scores
        data.append(row)

    table = msg.table(data, header=header, divider=True)
    return table


def _get_raw_results(dir: Path, model: str) -> List[Dict[str, Any]]:
    json_files = [f for f in dir.glob("**/*") if str(f.name).startswith(model)]
    msg.info(f"Found {len(json_files)} trials for model '{model}'")

    results = []
    for f in json_files:
        results.append(srsly.read_json(f))
    return results


def _summarize_results(
    results: List[Dict[str, Any]], per_entity_type: bool
) -> Dict[str, Tuple[float, float]]:
    def _collate(
        results: List[Dict[str, Any]], metrics: List[str]
    ) -> Dict[str, List[float]]:
        """Collect results into a single list"""
        summary = {}
        for metric in metrics:
            summary[metric] = []
            for result in results:
                summary[metric].append(result[metric])
        return summary

    # Compute for mean and standard deviation
    def _get_summary_metrics(
        summary: Dict[str, List]
    ) -> Dict[str, Tuple[float, float]]:
        """Compute for mean and stdev"""
        summary = {
            metric: (statistics.mean(scores), statistics.stdev(scores))
            for metric, scores in summary.items()
        }
        return summary

    summary = {}
    if per_entity_type:
        entities = results[0].get("ents_per_type").keys()
        metrics = ["p", "r", "f"]
        for entity in entities:
            per_entity_results = [
                result.get("ents_per_type").get(entity) for result in results
            ]
            summary[entity] = _get_summary_metrics(
                _collate(per_entity_results, metrics)
            )
    else:
        metrics = ["ents_p", "ents_r", "ents_f", "speed"]
        summary = _get_summary_metrics(_collate(results, metrics))
    return summary


if __name__ == "__main__":
    typer.run(collate_results)
