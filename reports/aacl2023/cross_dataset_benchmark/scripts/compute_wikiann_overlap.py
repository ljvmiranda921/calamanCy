from pathlib import Path
from typing import Iterable

import spacy
import srsly
import typer
from spacy.scorer import Scorer
from spacy.tokens import Doc, DocBin
from spacy.training.example import Example
from wasabi import msg

LABELS = ["PER", "ORG", "LOC"]


def compute_wikiann_overlap(
    # fmt: off
    references: Path = typer.Argument(..., help="Path to spaCy file containing reference annotations."),
    predictions: Path = typer.Argument(..., help="Path to spaCy file containing predicted / corrected annotations."),
    output_path: Path = typer.Option(None, "-o", "--output-path", help="Path to save scores in a JSONL file."),
    dedupe: bool = typer.Option(False, "-d", "--dedupe", help="Dedupe files (more accurate reporting)."),
    lang: str = typer.Option("tl", "-l", "--lang", help="Language code for vocab."),
    # fmt: on
):
    nlp = spacy.blank(lang)
    references = DocBin().from_disk(references).get_docs(nlp.vocab)
    predictions = DocBin().from_disk(predictions).get_docs(nlp.vocab)

    if dedupe:
        references = _dedupe(references)
        predictions = _dedupe(predictions)

    # Create Example objects for evaluation
    examples = []
    for pred, ref in zip(predictions, references):
        if pred.text == ref.text:
            eg = Example(pred, ref)
            examples.append(eg)

    scores = Scorer.score_spans(examples, "ents")
    msg.text(title="Scores", text=scores)

    if output_path:
        srsly.write_json(output_path, scores)
        msg.good(f"Saved metrics to {output_path}")


def _dedupe(docs: Iterable[Doc]) -> Iterable[Doc]:
    """Remove duplicates give a list of Documents"""
    docs = list(docs)
    old_length = len(docs)

    seen = set()
    deduped_docs = []
    for doc in docs:
        if doc.text not in seen:
            seen.add(doc.text)
            deduped_docs.append(doc)

    msg.good(f"Deduped into {len(deduped_docs)} (from {old_length})")
    return deduped_docs


if __name__ == "__main__":
    typer.run(compute_wikiann_overlap)
