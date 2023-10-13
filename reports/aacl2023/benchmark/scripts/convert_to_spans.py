"""Copy Doc.ents into Doc.spans"""

from copy import copy
from pathlib import Path

import spacy
import typer
from spacy.tokens import DocBin


def convert_to_spans(
    infile: Path,
    outfile: Path,
    lang=typer.Option("tl", "--lang", "-l", help="Language code"),
    spans_key=typer.Option("sc", "--spans-key", help="Spans key"),
):
    nlp = spacy.blank(lang)

    doc_bin = DocBin().from_disk(infile)
    docs = list(doc_bin.get_docs(nlp.vocab))

    _docs = []
    for doc in docs:
        _doc = copy(doc)
        _doc.spans[spans_key] = list(doc.ents)
        _docs.append(_doc)

    _doc_bin = DocBin(docs=_docs)
    _doc_bin.to_disk(outfile)


if __name__ == "__main__":
    typer.run(convert_to_spans)
