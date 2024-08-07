from pathlib import Path
from typing import List, Optional

import spacy
import typer
from spacy.tokens import DocBin
from wasabi import msg

from .utils import setup_gpu


def annotate(
    # fmt: off
    files: List[Path] = typer.Argument(..., help="Files (in spaCy format) to annotate."),
    model_path: Path = typer.Option(..., "--model", "--model-path", "-m", help="Model path to apply to the dataset."),
    output_dir: Optional[Path] = typer.Option(None, "--output", "--output-dir", "-o", help="Directory to save the annotated output in spaCy format."),
    gpu_id: int = typer.Option(-1, "--gpu", "--gpu-id", "-g", help="Set the GPU ID.", show_default=True),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Print extra output to console."),
    # fmt: on
):
    """Annotate a dataset given a model"""
    setup_gpu(gpu_id, verbose)
    nlp = spacy.load(model_path)
    for file in files:
        doc_bin = DocBin().from_disk(file)
        docs = doc_bin.get_docs(nlp.vocab)
        msg.info(f"Annotating file: {file} ({len(doc_bin)} documents)")

        annotated_docbin = DocBin()
        for doc in nlp.pipe(docs):
            annotated_docbin.add(doc)
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / file.name
            annotated_docbin.to_disk(output_path)
            msg.good(f"Saved annotated documents to {output_path}")


if __name__ == "__main__":
    typer.run(annotate)
