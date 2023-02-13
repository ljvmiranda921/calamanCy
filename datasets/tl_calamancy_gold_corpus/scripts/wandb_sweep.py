from pathlib import Path
from typing import Optional

import typer
import wandb
from spacy import util
from spacy.cli._util import parse_config_overrides
from spacy.training.initialize import init_nlp
from spacy.training.loop import train
from thinc.api import Config

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
    wandb_config: Path = typer.Option(DEFAULT_WANDB_CONFIG, "--wandb-config", "--config", "-C", help="Path to the WandB YAML configuration file."),
    output_path: Optional[Path] = typer.Option(None, "--output-path", "-o", help="Path to store the trained models."),
    gpu_id: int = Opt(0, "--gpu-id", "-G", help="Set the GPU ID. Use -1 for CPU."),
    # fmt: on
):
    """Perform a WandB sweep given a sweep config and a spaCy configuration"""
    overrides = parse_config_overrides(ctx.args)
    loaded_local_config = util.load_config(default_config, overrides=overrides)
    with wandb.init(config=str(wandb_config)) as run:
        sweeps_config = Config(util.dot_to_dict(run.config))
        merged_config = Config(loaded_local_config).merge(sweeps_config)
        nlp = init_nlp(merged_config, use_gpu=gpu_id)
        if output_path:
            output_path.mkdir(parents=True, exist_ok=True)
        train(nlp, output_path=output_path, use_gpu=gpu_id)


if __name__ == "__main__":
    app()
