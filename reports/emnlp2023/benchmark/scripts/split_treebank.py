"""Split treebank into train, dev, and test partitions

The spaCy library requires a validation set during training. This script
attempt provides this utility.
"""


import random
from pathlib import Path
from typing import List, Optional

import spacy
import typer
from spacy.tokens import Doc, DocBin
from wasabi import msg


def split_treebank(
    # fmt: off
    infile: Path = typer.Argument(..., help="Path to spaCy file to split."),
    outdir: Path = typer.Argument(..., help="Directory to store the outputs."),
    seed: Optional[int] = typer.Option(None, "--seed", help="Random seed for shuffling. Will not shuffle if nothing is passed."),
    lang: str = typer.Option("tl", "--lang", help="Language code to use for initializing the pipeline."),
    train_size: float = typer.Option(0.8, "--train-size", help="Size of the training set."),
    # fmt: on
):
    nlp = spacy.blank(lang)
    docs = list(DocBin().from_disk(infile).get_docs(nlp.vocab))

    if seed:
        msg.text(f"Shuffling using random seed `{seed}`")
        random.seed(seed)
        random.shuffle(docs)

    train_count = int(train_size * len(docs))

    train_docs = docs[:train_count]
    dev_docs = docs[train_count:]
    msg.text(f"Train size: {len(train_docs)}, dev size: {len(dev_docs)}")

    def _save_to_disk(docs: List[Doc], outfile: Path):
        doc_bin = DocBin(docs=docs)
        doc_bin.to_disk(outfile)
        msg.good(f"Saved to {str(outfile)}")

    _save_to_disk(train_docs, outdir / "train.spacy")
    _save_to_disk(dev_docs, outdir / "dev.spacy")


if __name__ == "__main__":
    typer.run(split_treebank)
