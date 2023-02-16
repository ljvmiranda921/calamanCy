from pathlib import Path
from typing import Optional

import typer
import wandb
from spacy import util
from spacy.cli._util import parse_config_overrides
from spacy.training.initialize import init_nlp
from spacy.training.loop import train
from srsly import read_yaml
from thinc.api import Config
from wasabi import msg

Arg = typer.Argument
Opt = typer.Option

DEFAULT_WANDB_CONFIG = Path().parent / "configs" / "sweeps" / "sweep.yml"

app = typer.Typer()


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def wandb_sweep(
    # fmt: off
    ctx: typer.Context,
    default_config: Path = typer.Argument(..., help="Path to the spaCy training configuration."), 
    sweep_id: Optional[str] = typer.Option(None, "--sweep-id", "--id", help="Agent id to resume an already started sweep."),
    wandb_config: Path = typer.Option(DEFAULT_WANDB_CONFIG, "--wandb-config", "--config", "-C", help="Path to the WandB YAML configuration file."),
    num_trials: int = typer.Option(30, "--num-trials", "-n", help="Number of trials to run the each hyperparameter combination."),
    project_name: str = typer.Option("calamanCy", help="Project name to save the sweep results."),
    output_path: Optional[Path] = typer.Option(None, "--output-path", "-o", help="Path to store the trained models."),
    gpu_id: int = Opt(0, "--gpu-id", "-G", help="Set the GPU ID. Use -1 for CPU."),
    # fmt: on
):
    """Perform a WandB sweep given a sweep config and a spaCy configuration"""
    overrides = parse_config_overrides(ctx.args)

    def train_spacy():
        loaded_local_config = util.load_config(default_config, overrides=overrides)
        with wandb.init(project=project_name) as run:
            sweeps_config = Config(util.dot_to_dict(run.config))
            merged_config = Config(loaded_local_config).merge(sweeps_config)
            nlp = init_nlp(merged_config, use_gpu=gpu_id)
            if output_path:
                output_path.mkdir(parents=True, exist_ok=True)
            train(nlp, output_path=output_path, use_gpu=gpu_id)

    sweep_config = dict(read_yaml(wandb_config))
    if not sweep_id:
        msg.info("Creating a new sweep")
        sweep_id = wandb.sweep(sweep_config, project=project_name)

    msg.info(f"Running sweep {sweep_id} for project '{project_name}'")
    wandb.agent(sweep_id, train_spacy, project=project_name, count=num_trials)


if __name__ == "__main__":
    app()
