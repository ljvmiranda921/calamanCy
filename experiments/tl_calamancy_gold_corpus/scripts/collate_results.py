import statistics
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import srsly
import typer
from wasabi import msg

Arg = typer.Argument
Opt = typer.Option


class Dataset(str, Enum):
    test = "test"
    dev = "dev"


def collate_results(
    # fmt: off
    input_path: Path = Arg(..., help="Path to a metrics directory with trials."),
    output_path: Optional[Path] = Opt(None, "--output-path", "--output", "-o", help="Optional path to save the summarized results as JSON."),
    dataset: Dataset = Opt(Dataset.test, "--dataset", "-d", help="Dataset type to summarize results upon."),
    per_entity_type: bool = Opt(False, "--per-entity-type", "-E", help="Show results per entity type."),
    # fmt: on
):
    """Summarize results given a metrics folder"""
    results, n_trials = _get_raw_results(input_path, dataset.value)
    summary_metrics = _summarize_results(results, False)
    _format_table(summary_metrics)
    if per_entity_type:
        per_entity_metrics = _summarize_results(results, True)
        _format_entity_table(per_entity_metrics)
    if output_path:
        results = {
            "n_trials": n_trials,
            "summary": summary_metrics,
            "per_entity": per_entity_metrics,
        }
        srsly.write_json(output_path, results)


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


def _get_raw_results(dir: Path, dataset: str) -> Union[List[Dict[str, Any]], int]:
    json_files = [f for f in dir.glob(f"**/*_{dataset}.json")]
    n_trials = len(json_files)
    msg.info(f"Found {n_trials} trials")

    results = []
    for f in json_files:
        results.append(srsly.read_json(f))
    return results, n_trials


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
