from pathlib import Path

import spacy
import srsly
import typer
from spacy.tokens import DocBin
from wasabi import msg


def spacy2jsonl(infile: Path, outfile: Path):
    """Convert spaCy files into JSONL for Prodigy"""
    nlp = spacy.blank("tl")
    doc_bin = DocBin().from_disk(infile)
    docs = doc_bin.get_docs(nlp.vocab)

    examples = [{"text": doc.text} for doc in docs]
    srsly.write_jsonl(outfile, examples)
    msg.good(f"Converted {infile} to {outfile}")


if __name__ == "__main__":
    typer.run(spacy2jsonl)
