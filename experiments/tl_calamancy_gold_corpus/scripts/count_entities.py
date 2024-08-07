from collections import Counter
from pathlib import Path

import spacy
import typer
from spacy.tokens import DocBin
from wasabi import msg

Arg = typer.Argument
Opt = typer.Option


def count_entities(
    input_path: Path = typer.Argument(..., help="Path to the spaCy file."),
    lang: str = Opt("tl", "--lang", "-l", help="Language code for Tagalog."),
):
    nlp = spacy.blank(lang)
    doc_bin = DocBin().from_disk(input_path)
    docs = doc_bin.get_docs(nlp.vocab)

    counter = Counter()
    tokens = 0
    for doc in docs:
        tokens += len(doc)
        for ent in doc.ents:
            if ent.label_ not in counter.keys():
                counter[ent.label_] = 1
            else:
                counter[ent.label_] += 1

    msg.info(
        f"Found {len(doc_bin)} documents with {tokens} tokens: {_format_counts(counter)}"
    )


def _format_counts(counter: Counter) -> str:
    return ", ".join([f"{k} ({v})" for k, v in counter.items()])


if __name__ == "__main__":
    typer.run(count_entities)
