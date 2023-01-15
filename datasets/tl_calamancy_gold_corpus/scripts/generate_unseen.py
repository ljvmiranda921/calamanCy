from pathlib import Path
from typing import Dict, Iterable, Optional, Set

import spacy
import typer
from spacy.tokens import Doc, DocBin
from wasabi import msg

Arg = typer.Argument
Opt = typer.Option


def generate_unseen(
    # fmt: off
    train_path: Path = Arg(..., help="Path to the training spaCy documents."),
    dev_path: Path = Arg(..., help="Path to the dev spaCy documents."),
    test_path: Path = Arg(..., help="Path to the test spaCy documents."),
    output_dir: Optional[Path] = Opt(None, "--output-dir", "-o", help="Directory to save seen and unseen splits."),
    lang: str = Opt("tl", "--lang", "-l", help="Language code."),
    # fmt: on
):
    """Generate unseen and seen splits for the dev and test data"""
    nlp = spacy.blank(lang)
    vocab = nlp.vocab
    paths = {"train": train_path, "dev": dev_path, "test": test_path}
    doc_bins = {dataset: DocBin().from_disk(path) for dataset, path in paths.items()}
    docs = {dataset: doc_bin.get_docs(vocab) for dataset, doc_bin in doc_bins.items()}

    train_ents = set()
    all_ents = 0
    for doc in docs.get("train"):
        all_ents += len(doc.ents)
        ents = {span.text for span in doc.ents}
        train_ents.update(ents)

    msg.text(f"Collected {len(train_ents)} unique entities from a total of {all_ents}.")

    # Create unseen and seen split for dev and test datasets
    datasets_to_split = ["dev", "test"]
    unseen_docs = {
        dataset: _mark_as_missing(docs=_docs, seen=train_ents, mark_seen=True)
        for dataset, _docs in docs.items()
        if dataset in datasets_to_split
    }
    seen_docs = {
        dataset: _mark_as_missing(docs=_docs, seen=train_ents, mark_seen=False)
        for dataset, _docs in docs.items()
        if dataset in datasets_to_split
    }

    # Save to disk
    if output_dir:
        _to_disk(unseen_docs, output_dir=output_dir / "unseen")
        _to_disk(seen_docs, output_dir=output_dir / "seen")


def _mark_as_missing(
    docs: Iterable[Doc],
    seen: Set[str],
    mark_seen: bool = True,
) -> DocBin:
    """
    Marks some of the ents in the input Doc objects as missing.  If 'mark_seen'
    is True then it marks entities in 'seen' as missing, otherwise it marks the
    entities not in 'seen' as missing.
    """
    doc_bin = DocBin()
    for doc in docs:
        if len(doc.ents) != 0:
            missing = []
            for ent in doc.ents:
                if not mark_seen ^ (ent.text in seen):
                    missing.append(ent)
            doc.set_ents([], missing=missing, default="unmodified")
        doc_bin.add(doc)
    return doc_bin


def _to_disk(docs_dict: Dict[str, DocBin], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    for dataset, doc_bin in docs_dict.items():
        output_path = output_dir / f"{dataset}.spacy"
        doc_bin.to_disk(output_path)
        msg.good(f"Saved {len(doc_bin)} to {output_path}")


if __name__ == "__main__":
    typer.run(generate_unseen)
