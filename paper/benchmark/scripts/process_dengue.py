"""Process the Dengue dataset

I want to note some post-processing issues in this dataset. If you inspect the
raw data from the source, you'll notice some blank lines that suggest that two
rows should be merged. However, the official Huggingface source:
https://huggingface.co/datasets/dengue_filipino suggests to just ignore
these lines.

I opted to not use the Huggingface source because the test split is incorrect.
It shows 4.02k rows when it should be 500.
"""

import csv
from collections import Counter
from pathlib import Path
from typing import Dict

import spacy
import typer
from spacy.tokens import DocBin
from srsly import write_jsonl
from wasabi import msg

# Filenames for the three splits
SPLIT_FILENAMES = ("train.csv", "test.csv", "dev.csv")
CATEGORIES = ["absent", "dengue", "health", "mosquito", "sick"]


def process_dengue(
    # fmt: off
    indir: Path = typer.Argument(..., help="Path to the unzipped dengue dataset containing the split CSV files."),
    outdir: Path = typer.Argument(..., help="Path to save the converted outputs."),
    include_pretraining: bool = typer.Option(False, "-pt", "--include-pretraining", help="Create pretraining corpora."),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Show additional information.")
    # fmt: on
):
    """Convert the Dengue dataset into the spaCy format"""
    pretraining_corpora = []
    for filename in SPLIT_FILENAMES:
        # Read examples from CSV file
        infile = indir / filename
        examples = []
        with open(infile) as f:
            reader = csv.reader(f, delimiter=",")
            line_count = 0

            for row in reader:
                if line_count == 0:
                    msg.text(
                        f"Column names are '{','.join(row)}' ({indir / filename})",
                        show=verbose,
                    )
                    categories_in_file = row[1:]
                    assert CATEGORIES == categories_in_file
                    line_count += 1
                else:
                    if len(row) == len(CATEGORIES) + 1:
                        examples.append(row)
                    line_count += 1

        # Convert examples into spaCy Doc objects
        doc_bin = DocBin()
        nlp = spacy.blank("tl")
        for text, *labels in examples:
            pretraining_corpora.append({"text": text})
            doc = nlp.make_doc(text)
            doc.cats = {cat: int(label) for cat, label in zip(CATEGORIES, labels)}
            doc_bin.add(doc)

        # Save the DocBin to disk
        if not outdir.is_dir():
            outdir.mkdir(parents=True, exist_ok=True)
        outfile = outdir / f"{infile.stem}.spacy"
        doc_bin.to_disk(outfile)

        counts = _count_total_cats(doc_bin, nlp)
        counts_msg = ", ".join(
            [f"{cat} ({count})" for cat, count in dict(counts).items()]
        )
        msg.good(f"Saved {len(doc_bin)} documents to {outfile} ({counts_msg})")

    if include_pretraining:
        write_jsonl(outdir / "pretraining.jsonl", lines=pretraining_corpora)
        msg.good(f"Saved pretraining corpora to {outdir / 'pretraining.jsonl'}")


def _count_total_cats(doc_bin: DocBin, nlp) -> Dict[str, int]:
    total_counts = Counter({category: 0 for category in CATEGORIES})
    for doc in doc_bin.get_docs(nlp.vocab):
        total_counts.update(doc.cats)

    return dict(total_counts)


if __name__ == "__main__":
    typer.run(process_dengue)
