import random
from itertools import groupby
from mmap import mmap
from pathlib import Path
from typing import List, Optional, Dict, Tuple
from math import ceil

import spacy
import typer
from spacy.tokens import Doc, DocBin
from tqdm import tqdm
from wasabi import msg

from .utils import setup_gpu

DELIMITER = "="


def process_tlunified(
    # fmt: off
    input_file: Path = typer.Argument(..., help="Path to the input text file."),
    filename: str = typer.Option("tlunified", "--filename", "-f", help="Filename to save the TLUnified corpus."),
    output_dir: Optional[Path] = typer.Option(None, "--output", "--output-dir", "-o", help="Directory to save the processed corpus."),
    segment: bool = typer.Option(False, "--segment", help="Segment documents into individual sentences."),
    seed: int = typer.Option(42, "--seed", help="Set the random seed for splitting.", show_default=True),
    splits: Tuple[float, float, float] = typer.Option((0.8, 0.1, 0.1), "--splits", help="Split ratio for train/validation/test partitions.", show_default=True),
    shuffle: bool = typer.Option(False, "--shuffle", help="Shuffle the texts before splitting."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Print extra output to console."),
    gpu_id: int = typer.Option(-1, "--gpu", "-g", help="Set the GPU ID.", show_default=True)
    # fmt: on
):
    """Split the TLUnified dataset and save it into the spaCy format

    The TLUnified dataset contains news articles from different media outlets in
    the Philippines. If the `--segment` flag is set, then this processor
    segments each document to individual sentences. Each document is delimited
    by the `=` symbol.
    """
    msg.info("Processing the TLUnified dataset")
    setup_gpu(gpu_id, silent=verbose)
    texts = read_dataset(input_file)
    texts = clean_corpus(texts, segment=segment, verbose=verbose)
    text_splits = split_dataset(
        texts, splits=splits, seed=seed, shuffle=shuffle, show=verbose
    )
    for split, txts in text_splits.items():
        msg.text(f"Split {split} has {len(txts)} documents", show=verbose)

    # Convert to spaCy Docs
    nlp = spacy.blank("tl")
    msg.text("Converting to spaCy Doc objects", show=verbose)
    text_docs = {split: nlp.pipe(txts) for split, txts in text_splits.items()}

    # Save to DocBin
    msg.text("Saving to DocBin", show=verbose)
    text_docbin = {split: DocBin(docs=docs) for split, docs in text_docs.items()}

    # Save to disk
    if output_dir:
        msg.text("Saving to disk", show=verbose)
        for split, doc_bin in text_docbin.items():
            output_path = output_dir / f"{filename}-{split}.spacy"
            output_dir.mkdir(parents=True, exist_ok=True)
            doc_bin.to_disk(output_path)
            msg.good(f"Saved to {output_path} ({len(doc_bin)} documents)")


def read_dataset(filepath: Path) -> List[str]:
    """Read the dataset from a given filepath"""

    def _get_num_lines(fp: Path) -> int:
        _fp = fp.open("r+")
        buf = mmap(_fp.fileno(), 0)
        lines = 0
        while buf.readline():
            lines += 1
        return lines

    texts = []
    with filepath.open("r") as f:
        for text in tqdm(f, total=_get_num_lines(filepath)):
            texts.append(text.rstrip())
    return texts


def clean_corpus(texts: List[str], segment: bool, verbose: bool) -> List[str]:
    """Clean the TLUnified corpus by removing empty strings, formatting titles, and more."""

    def _is_title(s: str) -> bool:
        """Check if a string is an article title"""
        if s[0] == DELIMITER and s[-1] == DELIMITER:
            return True
        else:
            return False

    def _clean_titles(texts: List[str]) -> List[str]:
        """Clean a list of texts by removing the delimiter in the title."""
        cleaned_texts = []
        for text in texts:
            if _is_title(text):
                cleaned_texts.append(text[1:-1].lstrip(" ").rstrip(" "))
            else:
                cleaned_texts.append(text)
        return cleaned_texts

    def _combine_texts(lines: List[str], delimiter="=") -> List[str]:
        """Combine the texts based on the delimiter"""
        _texts = [
            list(group)
            for key, group in groupby(lines, lambda x: _is_title(x))
            if not key
        ]
        titles = [line for line in lines if _is_title(line)]
        if len(_texts) != len(titles):
            msg.warn(
                "For some reason, the number of delimited text (presumably the title) doesn't match "
                "up to the number of articles. For this reason, I will not include the title in the "
                "text itself."
            )

        texts = []
        for sents in tqdm(_texts):
            # Costly operation
            text = " ".join(sents)
            texts.append(text)
        return texts

    # Remove empty strings i.e.,
    msg.text("Removing empty strings", show=verbose)
    texts = [t for t in texts if t]

    # Concatenate sentences if need be
    if not segment:
        msg.info("Concatenating sentences (this might take long)")
        texts = _combine_texts(texts)

    # Clean titles and remove delimiters
    msg.text("Cleaning the titles and removing delimiters", show=verbose)
    texts = _clean_titles(texts)
    return texts


def split_dataset(
    texts: List[str],
    splits: Tuple[float, float, float] = (0.8, 0.1, 0.1),
    seed: int = 0,
    shuffle: bool = True,
    show: bool = True,
) -> Dict[str, List[str]]:
    """Split the dataset into train / validation / test partitions"""
    msg.text(f"Splitting the dataset into partitions ({splits})", show=show)
    if shuffle:
        if not seed:
            msg.fail("Must provide seed when shuffle is True", exits=1)

        rng = random.Random(seed)
        rng.shuffle(texts)

    if sum(splits) != 1.00:
        msg.fail(f"Split ratio must sum to 1. sum({splits}) != 1", exits=1)

    train_size, validation_size, test_size = splits

    n_samples = len(texts)
    n_test = ceil(test_size * n_samples)
    n_dev = ceil(validation_size * n_samples)
    n_train = n_samples - (n_test + n_dev)
    train = texts[:n_train]
    validation = texts[n_train : n_train + n_dev]
    test = texts[n_train + n_dev :]
    return {"train": train, "validation": validation, "test": test}


if __name__ == "__main__":
    typer.run(process_tlunified)
