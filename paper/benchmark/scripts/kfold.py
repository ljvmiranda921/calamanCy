from pathlib import Path
from typing import Any, List, Iterable, Optional

import typer
from spacy.cli._util import parse_config_overrides
from spacy.tokens import Doc, DocBin

app = typer.Typer()


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def kfold(
    # fmt: off
    ctx: typer.Context,
    corpus_dir: Path = typer.Argument(..., help="Path to directory of spaCy files to merge and run cross-validation on."),
    config_path: Path = typer.Argument(..., help="Path to the spaCy training configuration file."),
    output_path: Optional[Path] = typer.Option(None, "-o", "--output", help="Path to save the metrics."),
    n_folds: int = typer.Option(10, "-n", "--n-folds", help="Number of folds to split the corpus."),
    seed: Optional[int] = typer.Option(None, "-s", "--seed", help="If set, shuffle the merged corpus using the given seed."),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Print out additional information."),
    use_gpu: int = typer.Option(-1, "--gpu-id", "-g", help="GPU ID or -1 for CPU"),
    # fmt: on
):
    """
    Perform k-fold cross validation by training a model at each fold and then
    reporting the average across `n_folds`.

    The config file includes all settings and hyperparmeters used during
    training. To oeverride settings in the config, e.g., settings that point to
    local paths or that you want to experiment with, you can override them as
    command line options. For instance, --training.batch_size 128 overrides the
    value of "batch_size" in the block "[training]".
    """

    overrides = parse_config_overrides(ctx.args)
    corpus = merge_corpus(corpus_dir, seed=seed)
    train_kfold(
        corpus,
        config_path,
        n_folds=n_folds,
        output_path=output_path,
        use_gpu=use_gpu,
        overrides=overrides,
    )


def _chunk(arr: List[Any], chunks: int) -> Iterable[Any]:
    """Split a list into chunks of fairly equal number of elements

    arr (List[Any]): the array to chunk.
    chunks (int): the number of chunks to split.
    RETURNS (Iterable[Any]): the chunked splits.
    """
    k, m = divmod(len(arr), chunks)
    return (arr[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(chunks))


def merge_corpus(corpus_dir: Path, *, seed: int) -> List[Doc]:
    """Combine spaCy files into a single

    corpus_dir (Path): the path to the corpus containing the spaCy files.
    seed (int): If set, shuffle the merged corpus with the given seed.
    RETURNS (List[Doc]): the combined list of spaCy Doc objects.
    """
    pass


def train_kfold(corpus: List[Doc]):
    pass
