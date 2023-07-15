"""Script for merging the Ugnayan and TRG treebanks

I decided to merge these two treebanks because training on one over the other
will just lead to less diversity on the dataset. However, the combined treebank
is still tiny (around 1.3k tokens).
"""

import random
from pathlib import Path
from typing import List, Optional

import spacy
import typer
from spacy.tokens import DocBin
from wasabi import msg


def merge_treebanks(
    # fmt: off
    infiles: List[Path] = typer.Argument(..., help="Path to the spaCy file of treebanks for merging."),
    outfile: Path = typer.Argument(..., help="Output file to save the merged treebank."),
    seed: Optional[int] = typer.Option(None, "--seed", help="Random seed for shuffling. Will not shuffle if nothing is passed."),
    lang: str = typer.Option("tl", "--lang", help="Language code to use for initializing the pipeline."),
    # fmt: on
):
    nlp = spacy.blank(lang)
    msg.info(f"Merging {len(infiles)} files")

    merged_docs = []
    for infile in infiles:
        docs = list(DocBin().from_disk(infile).get_docs(nlp.vocab))
        msg.text(f"Treebank {infile} has {len(docs)} documents.")
        merged_docs += docs
    msg.info(f"Merged file has {len(merged_docs)} documents.")

    if seed:
        msg.text(f"Shuffling the documents using random seed `{seed}`")
        random.seed(seed)
        random.shuffle(merged_docs)

    merged_doc_bin = DocBin(docs=merged_docs)
    merged_doc_bin.to_disk(outfile)
    msg.good(f"Saved to {str(outfile)}")


if __name__ == "__main__":
    typer.run(merge_treebanks)
