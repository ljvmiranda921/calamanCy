from pathlib import Path

import spacy
import typer
from spacy.tokens import Doc, DocBin
from spacy.util import get_words_and_spaces
from srsly import read_jsonl
from wasabi import msg

Arg = typer.Argument
Opt = typer.Option


def preprocess(
    # fmt: off
    input_path: Path = Arg(..., help="Path to the raw annotations (JSONL) file."),
    output_dir: Path = Arg(..., exists=True, help="Directory to save the corpus in spaCy format."),
    lang: str = Opt("tl", "--lang", "-l", help="Language code for Tagalog."),
    train_size: float = Opt(0.8, "--train-size", "-sz", help="Size of the training set."),
    shuffle: bool = Opt(False, "--shuffle", "-S", help="Shuffle before splitting."),
    seed: int = Opt(42, "--seed", "-s", help="Random seed when shuffling."),
    # fmt: on
):
    """Convert raw annotations into spaCy file with train-dev-test splits"""
    nlp = spacy.blank(lang)
    doc_bin = DocBin(attrs=["ENT_IOB", "ENT_TYPE"])
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
        doc_bin.add(doc)

    msg.info(f"Found {len(doc_bin)} documents.")
    breakpoint()


if __name__ == "__main__":
    typer.run(preprocess)
