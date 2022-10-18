from itertools import groupby
from mmap import mmap
from pathlib import Path
from typing import List, Optional

import typer
from spacy.tokens import Doc, DocBin
from tqdm import tqdm
from wasabi import msg

DELIMITER = "="


def process_tlunified(
    # fmt: off
    input_file: Path = typer.Argument(..., help="Path to the input text file."),
    filename: str = typer.Option("tlunified", "--filename", "-f", help="Filename to save the TLUnified corpus."),
    output_dir: Optional[Path] = typer.Option(None, "--output", "--output-dir", "-o", help="Directory to save the processed corpus."),
    seed: int = typer.Option(0, "--seed", help="Set the random seed for splitting.", show_default=True),
    segment: bool = typer.Option(False, "--segment", help="Segment documents into individual sentences."),
    # fmt: on
):
    """Split the TLUnified dataset and save it into the spaCy format

    The TLUnified dataset contains news articles from different media outlets in
    the Philippines. If the `--segment` flag is set, then this processor
    segments each document to individual sentences. Each document is delimited
    by the `=` symbol.
    """
    texts = []
    with input_file.open("r") as file:
        for text in tqdm(file, total=_get_num_lines(input_file)):
            texts.append(text.rstrip())

    # Remove empty strings i.e., ''
    texts[:] = [t for t in texts if t]

    # Concatenate sentences if need be
    if not segment:
        msg.info("Concatenating sentences (this might take long)")
        texts = _combine_texts(texts)

    # Clean delimiters
    texts = [
        text.removeprefix(DELIMITER).removesuffix(DELIMITER)
        for text in texts
        if _is_title(text)
    ]

    breakpoint()


def _is_title(s: str) -> bool:
    """Check if a string is an article title"""
    if s[0] == DELIMITER and s[-1] == DELIMITER:
        return True
    else:
        return False


def _combine_texts(lines: List[str], delimiter="=") -> List[str]:
    """Combine the texts based on the delimiter

    After some checking, it seems that the number of delimited text doesn't
    match up to the number of articles. For this reason, I will not include the
    title in the text itself.
    """
    _texts = [
        list(group) for key, group in groupby(lines, lambda x: _is_title(x)) if not key
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


def _get_num_lines(fp: Path) -> int:
    _fp = fp.open("r+")
    buf = mmap(_fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1
    return lines


if __name__ == "__main__":
    typer.run(process_tlunified)
