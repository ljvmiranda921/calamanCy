import random
from math import ceil
from pathlib import Path
from typing import Any, List, Optional, Sequence, Tuple

import spacy
import typer
from spacy.tokens import Doc, DocBin
from spacy.util import get_words_and_spaces
from srsly import read_jsonl
from wasabi import msg

Arg = typer.Argument
Opt = typer.Option


def _split_callback(value: Tuple[float, float, float]):
    if sum(value) != 1.0:
        raise typer.BadParameter(
            "Split sizes for train, dev, and test should sum up to 1.0 "
            f"({' + '.join(map(str, value))} != 1.0)",
        )
    return value


def preprocess(
    # fmt: off
    input_path: Path = Arg(..., help="Path to the raw annotations (JSONL) file."),
    output_dir: Path = Arg(..., exists=True, help="Directory to save the corpus in spaCy format."),
    lang: str = Opt("tl", "--lang", "-l", help="Language code for Tagalog."),
    split_size: Tuple[float, float, float] = Opt((0.8, 0.1, 0.1), "--split-size", "--sz", help="Split sizes for train, dev, and test respectively.", callback=_split_callback),
    shuffle: bool = Opt(False, "--shuffle", "-S", help="Shuffle before splitting."),
    seed: Optional[int] = Opt(None, "--seed", "-s", help="Random seed when shuffling."),
    # fmt: on
):
    """Convert raw annotations into spaCy file with train/dev/test splits"""
    nlp = spacy.blank(lang)
    docs = []
    for eg in read_jsonl(input_path):
        if eg["answer"] != "accept":
            continue
        tokens = [token["text"] for token in eg["tokens"]]
        words, spaces = get_words_and_spaces(tokens, eg["text"])
        doc = Doc(nlp.vocab, words=words, spaces=spaces)
        doc.ents = [
            doc.char_span(span["start"], span["end"], label=span["label"])
            for span in eg.get("spans", [])
        ]
        docs.append(doc)

    msg.info(f"Found {len(docs)} documents.")

    # Shuffle the dataset
    if shuffle:
        if seed:
            msg.text(f"Setting random seed to {seed}")
            random.seed(seed)
        msg.text(f"Shuffling the data")
        random.shuffle(docs)

    # Split the documents into train, dev, test
    train_size, dev_size, test_size = split_size
    train, dev, test = _train_dev_test_split(docs, train_size, dev_size, test_size)
    datasets = {"train": train, "dev": dev, "test": test}
    msg.text(
        f"Done splitting the train ({len(train)}), dev ({len(dev)}), "
        f" and test ({len(test)}) datasets!"
    )

    # Save to output_dir
    for dataset, docs in datasets.items():
        output_path = output_dir / f"{dataset}.spacy"
        doc_bin = DocBin(docs=docs, attrs=["ENT_IOB", "ENT_TYPE"])
        doc_bin.to_disk(output_path)
        msg.good(f"Saved {dataset} ({len(docs)}) dataset to {output_path}")


def _train_dev_test_split(
    data: Sequence[Any],
    train_size: float,
    dev_size: float,
    test_size: float,
) -> Tuple[List[Any], List[Any], List[Any]]:
    n_samples = len(data)
    n_test = ceil(test_size * n_samples)
    n_dev = ceil(dev_size * n_samples)
    n_train = n_samples - (n_test + n_dev)
    train = data[:n_train]
    dev = data[n_train : n_train + n_dev]
    test = data[n_train + n_dev :]
    return train, dev, test


if __name__ == "__main__":
    typer.run(preprocess)
