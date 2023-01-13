from pathlib import Path
from typing import Optional

import typer
from spacy.cli.project.run import project_run
from wasabi import msg

Arg = typer.Argument
Opt = typer.Option

NUM_TRIALS = 3


def benchmark(
    # fmt: off
    experiment_id: str = Arg(..., help="Experiment ID to keep track of the experiment."),
    num_trials: int = Opt(NUM_TRIALS, "--num-trials", "-n", help="Set the number of trials to run the experiment."),
    subcommand: str = Opt("ner", "--subcommand", "-C", help="Workflow command to run."),
    config: str = Opt("ner_chars.cfg", "--config", "-c", help="Name of the configuration file to use."),
    init_tok2vec: Optional[Path] = Opt(None, "--init-tok2vec", "-w", help="Path to the pretrained weights using the baseline configuration"), 
    vectors: Optional[Path] = Opt(None, "--vectors", "-v", help="Path to the initialized fastText static vectors."),
    trf_model_name: Optional[str] = Opt(None, "--trf-model-name", "--trf", help="Transformer model name from Huggingface."),
    gpu_id: int = Opt(0, "--gpu-id", "-G", help="Set the GPU ID. Use -1 for CPU."),
    force: bool = Opt(False, "--force", "-f", help="Force run the workflow."),
    dry_run: bool = Opt(False, "--dry-run", "--dry", help="Print the commands, don't run them."),
    # fmt: on
):
    """Run benchmarking script for a number of trials."""
    for trial_num in range(num_trials):
        msg.divider(f"Trial {trial_num}", icon="\u2600")
        overrides = {
            "vars.gpu_id": gpu_id,
            "vars.config": config,
            "vars.trial_num": trial_num,
            "vars.seed": trial_num,
            "vars.experiment_id": experiment_id,
        }

        if init_tok2vec:
            msg.text(f"Training with pretrained tok2vec weights: `{init_tok2vec}`")
            overrides["vars.init_tok2vec"] = str(init_tok2vec)

        if vectors:
            msg.text(f"Training with static vectors: `{vectors}`")
            overrides["vars.vectors"] = str(vectors)

        if trf_model_name:
            msg.text(f"Using transformer model: {trf_model_name}")
            overrides["vars.trf_model_name"] = trf_model_name

        project_run(
            project_dir=Path.cwd(),
            overrides=overrides,
            subcommand=subcommand,
            force=force,
            dry=dry_run,
        )


if __name__ == "__main__":
    typer.run(benchmark)
