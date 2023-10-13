"""
Utility script to run benchmark experiments

python -m scripts.benchmark all                  # Run all model configurations
python -m scripts.benchmark gpt4 cohere          # Run OpenAI GPT-4 and Cohere only
python -m scripts.benchmark all --ignore gpt4    # Run all except the GPT-4 config
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import typer
from spacy.cli.project.assets import project_assets
from spacy.cli.project.run import project_run
from wasabi import msg


@dataclass
class ModelConfig:
    family: str
    name: str


CONFIGS = {
    "gpt4": ModelConfig(family="spacy.GPT-4.v1", name="gpt-4"),
    "gpt3.5": ModelConfig(family="spacy.GPT-3-5.v1", name="gpt-3.5-turbo"),
    "cohere": ModelConfig(family="spacy.Command.v1", name="command"),
    "claude": ModelConfig(family="spacy.Claude-1.v1", name="claude-1"),
    "dolly": ModelConfig(family="spacy.Dolly.v1", name="dolly-v2-7b"),
    "llama2": ModelConfig(family="spacy.Llama2.v1", name="Llama-2-7b-hf"),
    "openllama": ModelConfig(family="spacy.OpenLLaMA.v1", name="open_llama_7b_v2"),
    "falcon": ModelConfig(family="spacy.Falcon.v1", name="falcon-7b"),
    "stablelm": ModelConfig(family="spacy.StableLM.v1", name="stablelm-base-alpha-7b"),
}

app = typer.Typer()
help_str = f"""
Utility script to run benchmark experiments.

You can choose a configuration among {', '.join([conf for conf in CONFIGS])}.
If you wish to run against all models, pass 'all'.
"""


def _callback_ignore(arg):
    return arg.split(",") if arg else None


@app.command(name="benchmark", help=help_str)
def benchmark(
    # fmt: off
    configs: List[str] = typer.Argument(..., help="LLM configuration to run the pipeline on."),
    subcommand: str = typer.Option("all",  "-C", "--subcommand", "--command", help="Subcommand to run. Defaults to 'all'."),
    ignore: Optional[str] = typer.Option(None, "--ignore", help="Ignore a specific config. Useful when running 'all'", callback=_callback_ignore),
    dry: bool = typer.Option(False, "--dry", help="Perform a dry run and do not execute the commands."),
    force: bool = typer.Option(False, "-f", "--force", help="Force run a spaCy workflow."),
    # fmt: on
):
    root = Path(__file__).parent.parent
    project_assets(root)

    if "all" in configs:
        msg.info("Configuration set to 'all'. Will run all model configurations.")
        configs = list(CONFIGS.keys())

    if ignore:
        configs = [conf for conf in configs if conf not in ignore]

    msg.info(
        f"Running on the following configurations: {', '.join([conf for conf in configs])}"
    )
    for config in configs:
        if config in CONFIGS:
            model = CONFIGS[config]
            msg.text(
                f"Running config '{config}' with the '{model.family}' model family"
                f" and '{model.name}' variant."
            )
            overrides = {
                "vars.model_family": model.family,
                "vars.model_name": model.name,
            }
            project_run(
                root,
                subcommand,
                capture=True,
                overrides=overrides,
                dry=dry,
                force=force,
            )

        else:
            msg.warn(
                f"Config '{config}' not found. Skipping...\n"
                f"Available configs: {', '.join([conf for conf in CONFIGS])}"
            )


if __name__ == "__main__":
    app()
