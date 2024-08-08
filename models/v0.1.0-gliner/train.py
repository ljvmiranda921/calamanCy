import typer
from pathlib import Path
from typing import Optional

import torch
from gliner import GLiNERConfig, GLiNER
from gliner.training import Trainer, TrainingArguments
from gliner.data_processing.collator import DataCollatorWithPadding, DataCollator
from gliner.utils import load_config_as_namespace
from gliner.data_processing import WordsSplitter, GLiNERDataset


def main(
    # fmt: off
    base_model: str = typer.Argument(..., help="Base model used for training."),
    output_dir: Path = typer.Argument(..., help="Path to store the output model."),
    checkpoint_dir: Path = typer.Option(Path("checkpoints"), help="Path for storing checkpoints."),
    push_to_hub: Optional[str] = typer.Option(None, help="If set, will upload the trained model to the provided Huggingface model namespace."),
    num_steps: int = typer.Option(500, help="Number of steps to run training."),
    batch_size: int = typer.Option(8, help="Batch size used for training."),
    # fmt: on
):
    pass


if __name__ == "__main__":
    typer.run(main)
