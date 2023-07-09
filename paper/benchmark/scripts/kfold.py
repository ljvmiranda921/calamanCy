import random
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import spacy
import typer
from spacy.cli._util import parse_config_overrides, show_validation_error
from spacy.tokens import Doc, DocBin
from spacy.training.corpus import Corpus
from spacy.training.initialize import init_nlp
from spacy.training.loop import train as train_nlp
from spacy.util import load_config
from srsly import write_json
from wasabi import msg

app = typer.Typer()

# Metrics we want to track
METRICS = ["token_acc", "pos_acc", "morph_acc", "tag_acc", "dep_uas", "dep_las"]


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
    metrics: str = typer.Option(",".join(METRICS), "-m", "--metrics", help="Comma-separated list of metrics we want to track.", callback=lambda x: x.split(",")),
    seed: Optional[int] = typer.Option(None, "-s", "--seed", help="If set, shuffle the merged corpus using the given seed."),
    lang: str = typer.Option("tl", "-l", "--lang", help="Language code for reading the spaCy files."),
    cache_dir: Optional[Path] = typer.Opion(None, "-c", "--cache-dir", "--cache", help="Optional path to save the spaCy documents at a given fold."),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Print out additional information."),
    use_gpu: int = typer.Option(-1, "--gpu-id", "-g", help="GPU ID or -1 for CPU"),
    # fmt: on
):
    """
    Perform k-fold cross validation by training a model at each fold and then
    reporting the average across 'n_folds'.

    The config file includes all settings and hyperparmeters used during
    training. To oeverride settings in the config, e.g., settings that point to
    local paths or that you want to experiment with, you can override them as
    command line options. For instance, --training.batch_size 128 overrides the
    value of "batch_size" in the block "[training]".

    You can also pass a value to the 'cache_dir' parameter to optionally save
    the spaCy files at the current fold.
    """
    overrides = parse_config_overrides(ctx.args)
    docs = merge_corpus(
        corpus_dir,
        seed=seed,
        lang=lang,
        verbose=verbose,
    )
    train_kfold(
        docs,
        config_path,
        n_folds=n_folds,
        output_path=output_path,
        metrics=metrics,
        use_gpu=use_gpu,
        overrides=overrides,
        cache_dir=cache_dir,
        verbose=verbose,
    )


def _chunk(arr: List[Any], chunks: int) -> Iterable[Any]:
    """Split a list into chunks of fairly equal number of elements.

    arr (List[Any]): the array to chunk.
    chunks (int): the number of chunks to split.
    RETURNS (Iterable[Any]): the chunked splits.
    """
    k, m = divmod(len(arr), chunks)
    return (arr[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(chunks))


def _get_all_except(idx: int, arr: List[Any]) -> List[Any]:
    """Get all elements of a list except a given index.

    idx (int): the index to ignore.
    arr (List[Any]): the list to get the elements from.
    RETURNS (List[Any]): the updated list.
    """
    return arr[:idx] + arr[(idx + 1) :]


def _flatten(arr: List[Any]) -> List[Any]:
    """Flatten a list of lists.

    arr (List[Any]): the list to flatten.
    RETURNS (List[Any]): the flattened list.
    """
    return [item for sublist in arr for item in sublist]


def merge_corpus(corpus_dir: Path, *, lang: str, seed: int, verbose: bool) -> List[Doc]:
    """Combine spaCy files into a single list.

    corpus_dir (Path): the path to the corpus containing the spaCy files.
    lang (str): language code to read the spaCy files.
    seed (int): if set, shuffle the merged corpus with the given seed.
    verbose (bool): flag to show additional information.
    RETURNS (List[Doc]): the combined list of spaCy Doc objects.
    """
    nlp = spacy.blank(lang)
    merged_docs = []
    for spacy_file in corpus_dir.glob("*.spacy"):
        msg.text(f"Found file '{spacy_file}'", show=verbose)
        doc_bin = DocBin().from_disk(spacy_file)
        docs = list(doc_bin.get_docs(nlp.vocab))
        merged_docs.extend(docs)

    if seed:
        msg.text(f"Shuffling Doc objects using seed '{seed}'", show=verbose)
        random.seed(seed)
        random.shuffle(merged_docs)  # shuffles inplace

    msg.text(f"Merged a total of {len(merged_docs)} documents")
    return merged_docs


def train_kfold(
    docs: List[Doc],
    config_path: Path,
    *,
    n_folds: int,
    output_path: Path,
    metrics: List[str],
    use_gpu: int,
    overrides: Dict[str, Any],
    cache_dir: Path,
    verbose: bool,
):
    """Train and evaluate using k-fold cross validation.

    docs (List[Doc]): spaCy documents to split and train from.
    config_path (Path): path to the spaCy training configuration file.
    n_folds (int): number of folds to create.
    output_path (Path): path to save the metrics file.
    metrics (List[str]): list of metrics we want to track for evaluation.
    use_gpu (int): the GPU machine to use. Set to -1 to use CPU.
    overrides (Dict[str, Any]): overrides to the configuration file.
    cache_dir (Path): optional path to save the created folds.
    verbose (bool): print out extra information.
    """
    folds = list(_chunk(docs, n_folds))
    scores_per_fold = {metric: [] for metric in metrics}
    msg.text(f"Tracking the following metrics: {','.join(scores_per_fold.keys())}")
    for idx, fold in enumerate(folds):
        dev = fold
        train = _flatten(_get_all_except(idx, arr=folds))
        msg.divider(f"Fold {idx+1}, train: {len(train)}, dev: {len(dev)}")

        with tempfile.TemporaryDirectory() as tmpdir:
            # Save the train and test corpora into a temporary directory then
            # train within the context of that directory.
            msg.text("Preparing data for training", show=verbose)
            overrides["paths.train"] = str(Path(tmpdir) / f"tmp_train-{idx+1}.spacy")
            overrides["paths.dev"] = str(Path(tmpdir) / f"tmp_dev-{idx+1}.spacy")
            DocBin(docs=train).to_disk(overrides.get("paths.train"))
            DocBin(docs=dev).to_disk(overrides.get("paths.dev"))
            if cache_dir:
                msg.text(f"Saving to {cache_dir}", show=verbose)
                DocBin(docs=train).to_disk(cache_dir / f"train-{idx+1}.spacy")
                DocBin(docs=dev).to_disk(cache_dir / f"dev-{idx+1}.spacy")
            msg.text(
                f"Temp files at {overrides.get('paths.train')} "
                f"and {overrides.get('paths.dev')}",
                show=verbose,
            )
            # Train the model for the current fold.
            msg.text(
                f"Training the model for the current fold: '{idx+1}'", show=verbose
            )
            with show_validation_error(config_path, hint_fill=False):
                config = load_config(config_path, overrides, interpolate=False)
                nlp = init_nlp(config)
            nlp, _ = train_nlp(nlp, None, use_gpu=use_gpu)

            # Perform evaluation
            msg.text(f"Evaluating on the development dataset", show=verbose)
            corpus = Corpus(overrides["paths.dev"], gold_preproc=False)
            examples = corpus(nlp)
            scores = nlp.evaluate(examples)

            for metric in metrics:
                if metric in scores:
                    scores_per_fold[metric].append(scores[metric])
                else:
                    msg.warn(
                        f"Metric '{metric}' not found in pipeline. "
                        f"Available metrics are: {','.join(scores.keys())}"
                    )
            msg.text(
                f"Scores for fold '{idx+1}'"
                f"{', '.join([f'{m}: {scores[m]}' for m in metrics if m in scores])}",
                show=verbose,
            )

    msg.info(f"Computing final {n_folds}-fold cross-validation score")
    avg_scores = {
        metric: sum(scores) / len(scores) for metric, scores in scores_per_fold.items()
    }
    msg.table(avg_scores, header=("Metric", "Score"))
    if output_path:
        write_json(output_path, avg_scores, indent=4)


if __name__ == "__main__":
    app()
