import subprocess
import sys
from pathlib import Path
from typing import Optional

import pandas as pd
import typer
from srsly import read_json
from wasabi import msg

TREEBANK_TRAIN = Path("corpus/treebank/tl_newscrawl-ud-train.spacy")
TREEBANK_DEV = Path("corpus/treebank/tl_newscrawl-ud-dev.spacy")
NER_TRAIN = Path("corpus/ner/train.spacy")
NER_DEV = Path("corpus/ner/dev.spacy")

DEP_TEST_SETS = {
    "newscrawl": Path("corpus/treebank/tl_newscrawl-ud-test.spacy"),
    "trg": Path("corpus/treebank/tl_trg-ud-test.spacy"),
    "ugnayan": Path("corpus/treebank/tl_ugnayan-ud-test.spacy"),
}
NER_TEST_SETS = {
    "tlunified": Path("corpus/ner/test.spacy"),
    "uner-trg": Path("corpus/ner/uner-trg-test.spacy"),
    "uner-ugnayan": Path("corpus/ner/uner-ugnayan-test.spacy"),
    "tfnerd": Path("corpus/ner/tfnerd-test.spacy"),
}
DEP_METRICS = ["lemma_acc", "tag_acc", "pos_acc", "morph_acc", "dep_uas", "dep_las"]
NER_METRICS = ["ents_p", "ents_r", "ents_f"]


def ablation_trf_model(
    # fmt: off
    model_names: str = typer.Argument("microsoft/mdeberta-v3-base,jhu-clsp/mmBERT-base,jhu-clsp/mmBERT-small", help="Comma-separated list of HuggingFace models to compare."),
    seeds: str = typer.Option("0,1,2", "--seeds", help="Comma-separated list of random seeds to train with."),
    output_dir: Path = typer.Option(Path("training/ablation_trf"), "--output-dir", help="Directory to store the trained pipelines."),
    evals_dir: Path = typer.Option(Path("evals/ablation_trf"), "--evals-dir", help="Directory to store the evaluation results."),
    gpu_id: int = typer.Option(0, "--gpu-id", help="GPU ID to use. On Apple Silicon, any non-negative value uses MPS."),
    max_steps: Optional[int] = typer.Option(None, "--max-steps", help="If set, overrides the number of training steps (useful for smoke tests)."),
    overwrite: bool = typer.Option(False, "--overwrite", help="If set, retrains pipelines even if they already exist."),
    # fmt: on
):
    """Compare transformer base models for tl_calamancy_trf"""
    for path in [TREEBANK_TRAIN, TREEBANK_DEV, NER_TRAIN, NER_DEV]:
        if not path.exists():
            msg.fail(f"Missing {path}. Run `spacy project run setup` first.", exits=1)

    for model_name in model_names.split(","):
        for seed in seeds.split(","):
            run_name = f"{model_name.split('/')[-1]}-seed{seed}"
            run_dir = output_dir / run_name
            msg.divider(run_name)

            for component, config, train, dev in [
                ("parser", "configs/parser_trf.cfg", TREEBANK_TRAIN, TREEBANK_DEV),
                ("ner", "configs/ner_trf.cfg", NER_TRAIN, NER_DEV),
            ]:
                model_dir = run_dir / component
                if (model_dir / "model-best").exists() and not overwrite:
                    msg.info(f"Found existing {model_dir}, skipping training")
                    continue
                cmd = [
                    sys.executable, "-m", "spacy", "train", config,
                    "--output", str(model_dir),
                    "--nlp.lang", "tl",
                    "--components.transformer.model.name", model_name,
                    "--system.seed", seed,
                    "--paths.train", str(train),
                    "--paths.dev", str(dev),
                    "--gpu-id", str(gpu_id),
                ]  # fmt: skip
                if max_steps:
                    cmd += [
                        "--training.max_steps", str(max_steps),
                        "--training.eval_frequency", str(max(1, min(200, max_steps // 2))),
                        "--training.optimizer.learn_rate.total_steps", str(max_steps),
                        "--training.optimizer.learn_rate.warmup_steps", str(max(1, max_steps // 10)),
                    ]  # fmt: skip
                msg.info(f"Training {component} for {run_name}")
                subprocess.run(cmd, check=True)

            evaluate(
                run_dir / "parser" / "model-best",
                "dep",
                DEP_TEST_SETS,
                evals_dir / run_name,
                gpu_id,
            )
            evaluate(run_dir / "ner" / "model-best", "ner", NER_TEST_SETS, evals_dir / run_name, gpu_id)  # fmt: skip

    summarize(evals_dir)


def evaluate(
    model_dir: Path,
    task: str,
    test_sets: dict[str, Path],
    outdir: Path,
    gpu_id: int,
):
    outdir.mkdir(parents=True, exist_ok=True)
    for dataset, test_path in test_sets.items():
        if not test_path.exists():
            msg.warn(f"Missing {test_path}, skipping. Run `spacy project run setup-eval-data` to create it.")  # fmt: skip
            continue
        cmd = [
            sys.executable, "-m", "spacy", "evaluate",
            str(model_dir), str(test_path),
            "--output", str(outdir / f"{task}_{dataset}.json"),
            "--gpu-id", str(gpu_id),
        ]  # fmt: skip
        subprocess.run(cmd, check=True)


def summarize(evals_dir: Path):
    """Aggregate the evaluation results across seeds (mean and standard deviation)"""
    rows = []
    for run_dir in evals_dir.iterdir():
        if run_dir.is_dir():
            model_name, seed = run_dir.name.rsplit("-seed", 1)
            for json_file in run_dir.glob("*.json"):
                task, dataset = json_file.stem.split("_")
                data = read_json(json_file)
                metrics = DEP_METRICS if task == "dep" else NER_METRICS
                row = {
                    "model": model_name,
                    "seed": seed,
                    "task": task,
                    "dataset": dataset,
                }
                row.update({metric: data.get(metric) for metric in metrics})
                rows.append(row)

    if not rows:
        msg.warn(f"No evaluation results found in {evals_dir}")
        return

    df = pd.DataFrame(rows)
    summary = []
    for task, metrics in [("dep", DEP_METRICS), ("ner", NER_METRICS)]:
        task_df = df[df["task"] == task]
        if task_df.empty:
            continue
        grouped = (
            task_df.groupby(["dataset", "model"])[metrics].agg(["mean", "std"]) * 100
        )
        table = pd.DataFrame(index=grouped.index)
        for metric in metrics:
            mean, std = grouped[(metric, "mean")], grouped[(metric, "std")].fillna(0)
            table[metric] = [f"{m:.2f} ({s:.2f})" for m, s in zip(mean, std)]
        table = table.reset_index()
        msg.text(f"Results for {task} (n_seeds={task_df['seed'].nunique()}):")
        print(table.to_markdown(index=False))
        summary.append(f"## {task}\n\n{table.to_markdown(index=False)}\n")

    summary_path = evals_dir / "summary.md"
    summary_path.write_text("\n".join(summary), encoding="utf-8")
    msg.good(f"Saved summary to {summary_path}")


if __name__ == "__main__":
    typer.run(ablation_trf_model)
