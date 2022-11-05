"""Experiment Runner for Benchmarking"""

from pathlib import Path
from typing import Optional
from copy import deepcopy

from spacy.cli.project.run import project_run
from spacy.cli._util import parse_config_overrides
import typer
from wasabi import msg

Arg = typer.Argument
Opt = typer.Option

app = typer.Typer()



@app.command(name="baseline")
def run_baseline(
    # fmt: off
    num_trials: int = Opt(1, "--num-trials", "-n", help="Set the number of trials to run the experiment.", show_default=True),
    subcommand: str = Opt("ner", "--subcommand", "-C", help="Workflow command to run.", show_default=True),
    config: str = Opt("baseline", "--config", "-c", help="Name of the baseline configuration.", show_default=True),
    init_tok2vec: Path = Opt(Path("assets/tlunified_pt_chars.bin"), "--init-tok2vec", "-w", help="Path to the pretrained weights using the baseline configuration", show_default=True), 
    gpu_id: int = Opt(0, "--gpu-id", "-G", help="Set the GPU ID. Use -1 for CPU.", show_default=True),
    force: bool = Opt(False, "--force", "-f", help="Force run the workflow."),
    dry_run: bool = Opt(False, "--dry-run", help="Print the commands, don't run them."),
    # fmt: on
):
    """Run baseline experiment

    This experiment trains a NER model with and without pretrained weights
    for a specified number of trials.
    """
    for trial_num in range(num_trials):
        overrides = {
            "--vars.gpu_id": gpu_id,
            "--vars.config": config,
            "--vars.trial_num": trial_num,
            "--vars.seed": trial_num,
        }

        # Run without pretrained weights
        baseline_n_pt = deepcopy(overrides)
        baseline_n_pt["--vars.experiment_id"] = "baseline_n_pt"
        project_run(
            project_dir=Path.cwd(), 
            overrides=parse_config_overrides(baseline_n_pt),
            subcommand=subcommand, 
            force=force, 
            dry=dry_run
        )

        # Run with pretrained weights
        baseline_y_pt = deepcopy(overrides)
        baseline_y_pt["--vars.experiment_id"] = "baseline_y_pt"
        baseline_y_pt["--vars.init_tok2vec"] = str(init_tok2vec)
        project_run(
            project_dir=Path.cwd(), 
            overrides=parse_config_overrides(baseline_y_pt),
            subcommand=subcommand, 
            force=force, 
            dry=dry_run
        )


