from pathlib import Path
from typing import Optional
from copy import deepcopy

from spacy.cli.project.run import project_run
import typer
from wasabi import msg

Arg = typer.Argument
Opt = typer.Option

HELP = """Suite of commands to run benchmarking experiments. By default, each experiment 
runs three trials across multiple seeds. The scores for each trial is saved separately."""
NUM_TRIALS = 3

app = typer.Typer(help=HELP)



@app.command(name="baseline", help="Run experiment without static vectors.")
def run_baseline(
    # fmt: off
    num_trials: int = Opt(NUM_TRIALS, "--num-trials", "-n", help="Set the number of trials to run the experiment.", show_default=True),
    subcommand: str = Opt("ner", "--subcommand", "-C", help="Workflow command to run.", show_default=True),
    config: str = Opt("baseline", "--config", "-c", help="Name of the baseline configuration.", show_default=True),
    init_tok2vec: Path = Opt(Path("assets/tlunified_pt_chars.bin"), "--init-tok2vec", "-w", help="Path to the pretrained weights using the baseline configuration", show_default=True), 
    gpu_id: int = Opt(0, "--gpu-id", "-G", help="Set the GPU ID. Use -1 for CPU.", show_default=True),
    force: bool = Opt(False, "--force", "-f", help="Force run the workflow."),
    dry_run: bool = Opt(False, "--dry-run", "--dry", help="Print the commands, don't run them."),
    # fmt: on
):
    """Run experiment without static vectors 
    
    This experiment runs the baseline configuration with and without pretrained
    weights for a given number of trials."""
    for trial_num in range(num_trials):
        msg.divider(f"Trial {trial_num}", icon="\u2600")
        overrides = {
            "vars.gpu_id": gpu_id,
            "vars.config": config,
            "vars.trial_num": trial_num,
            "vars.seed": trial_num,
        }

        # Run without pretrained weights
        msg.info("Running experiment without pretrained weights")
        baseline_n_pt = deepcopy(overrides)
        baseline_n_pt["vars.experiment_id"] = "baseline_n_pt"
        project_run(
            project_dir=Path.cwd(), 
            overrides=baseline_n_pt,
            subcommand=subcommand, 
            force=force, 
            dry=dry_run
        )

        # Run with pretrained weights
        msg.info("Running experiment with pretrained weights")
        baseline_y_pt = deepcopy(overrides)
        baseline_y_pt["vars.experiment_id"] = "baseline_y_pt"
        baseline_y_pt["vars.init_tok2vec"] = str(init_tok2vec)
        project_run(
            project_dir=Path.cwd(), 
            overrides=baseline_y_pt,
            subcommand=subcommand, 
            force=force, 
            dry=dry_run
        )



@app.command(name="fasttext")
def run_fasttext(
    # fmt: off
    num_trials: int = Opt(NUM_TRIALS, "--num-trials", "-n", help="Set the number of trials to run the experiment.", show_default=True),
    subcommand: str = Opt("ner", "--subcommand", "-C", help="Workflow command to run.", show_default=True),
    config: str = Opt("fasttext", "--config", "-c", help="Name of the baseline configuration.", show_default=True),
    init_tok2vec: Path = Opt(Path("assets/tlunified_pt_vects.bin"), "--init-tok2vec", "-w", help="Path to the pretrained weights using the baseline configuration", show_default=True), 
    vectors: Path = Opt(Path("vectors/fasttext-tl"), "--vectors", "-v", help="Path to the initialized fastText static vectors.", show_default=True),
    gpu_id: int = Opt(0, "--gpu-id", "-G", help="Set the GPU ID. Use -1 for CPU.", show_default=True),
    force: bool = Opt(False, "--force", "-f", help="Force run the workflow."),
    dry_run: bool = Opt(False, "--dry-run", help="Print the commands, don't run them."),
    # fmt: on
):
    """Run experiment with fastText vectors. 
    
    
    This experiment runs the baseline configuration with and without pretrained
    for a given number of trials."""
    for trial_num in range(num_trials):
        msg.divider(f"Trial {trial_num}", icon="\u2600")
        overrides = {
            "vars.gpu_id": gpu_id,
            "vars.config": config,
            "vars.trial_num": trial_num,
            "vars.seed": trial_num,
            "vars.vectors": vectors,
        }

        # Run without pretrained weights
        msg.info("Running experiment without pretrained weights")
        baseline_n_pt = deepcopy(overrides)
        baseline_n_pt["vars.experiment_id"] = "fasttext_n_pt"
        project_run(
            project_dir=Path.cwd(), 
            overrides=parse_config_overrides(baseline_n_pt),
            subcommand=subcommand, 
            force=force, 
            dry=dry_run
        )

        # Run with pretrained weights
        msg.info("Running experiment with pretrained weights")
        baseline_y_pt = deepcopy(overrides)
        baseline_y_pt["vars.experiment_id"] = "fasttext_y_pt"
        baseline_y_pt["vars.init_tok2vec"] = str(init_tok2vec)
        project_run(
            project_dir=Path.cwd(), 
            overrides=parse_config_overrides(baseline_y_pt),
            subcommand=subcommand, 
            force=force, 
            dry=dry_run
        )


if __name__ == "__main__":
    app()