"""Process the Hatespeech dataset

I want to note some post-processing issues in this dataset. If you inspect the
raw data from the source, you'll notice some blank lines that suggest that two
rows should be merged. However, the official Huggingface source:
https://huggingface.co/datasets/hate_speech_filipino suggests to just ignore
these lines.

I opted to not use the Huggingface source because the test split is incorrect.
It shows 10k rows when it should be 4.32k as reported in the paper.

The script below should ignore those blank lines and give the correct number of
examples for each split.
"""

import csv
from pathlib import Path

import spacy
import typer
from spacy.tokens import DocBin
from srsly import write_jsonl
from wasabi import msg

# Filenames for the three splits
SPLIT_FILENAMES = ("train.csv", "test.csv", "dev.csv")
CATEGORIES = {"HATESPEECH", "NOT_HATESPEECH"}


def process_hatespeech(
    # fmt: off
    indir: Path = typer.Argument(..., help="Path to the unzipped hatespeech dataset containing the split CSV files."),
    outdir: Path = typer.Argument(..., help="Path to save the converted outputs."),
    include_pretraining: bool = typer.Option(False, "-pt", "--include-pretraining", help="Create pretraining corpora."),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Show additional information.")
    # fmt: on
):
    """Convert the Hatespeech dataset into the spaCy format"""
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
                    line_count += 1
                else:
                    if len(row) == 2:
                        examples.append(row)
                    line_count += 1

        # Convert examples into spaCy Doc objects
        doc_bin = DocBin()
        nlp = spacy.blank("tl")
        # Note: positive here means positive examples (labeled as 1), not
        # positive sentiment.
        n_positive = 0
        n_negative = 0
        for text, label in examples:
            doc = nlp.make_doc(text)
            pretraining_corpora.append({"text": text})
            doc.cats = {category: 0 for category in CATEGORIES}
            if int(label) == 1:
                doc.cats["HATESPEECH"] = 1
                n_positive += 1
            else:
                doc.cats["NOT_HATESPEECH"] = 1
                n_negative += 1
            doc_bin.add(doc)

        # Save the DocBin to disk
        if not outdir.is_dir():
            outdir.mkdir(parents=True, exist_ok=True)
        outfile = outdir / f"{infile.stem}.spacy"
        doc_bin.to_disk(outfile)
        msg.good(
            f"Saved {len(doc_bin)} documents to {outfile} (HATESPEECH={n_positive}, NOT_HATESPEECH={n_negative})"
        )

    if include_pretraining:
        write_jsonl(outdir / "pretraining.jsonl", lines=pretraining_corpora)
        msg.good(f"Saved pretraining corpora to {outdir / 'pretraining.jsonl'}")


if __name__ == "__main__":
    typer.run(process_hatespeech)
