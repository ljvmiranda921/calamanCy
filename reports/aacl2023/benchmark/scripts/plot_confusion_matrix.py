from pathlib import Path
from wasabi import msg
from typing import Iterable

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import spacy
import typer
import numpy as np
from spacy.tokens import Doc, DocBin
from sklearn.metrics import confusion_matrix

from .constants import MATPLOTLIB_STYLE

pylab.rcParams.update(MATPLOTLIB_STYLE)


def plot_confusion_matrix(
    # fmt: off
    reference: Path = typer.Argument(..., help="Path to the spaCy file for the reference annotations."),
    model_path: Path = typer.Argument(..., help="Path to the model for getting the predictions."),
    outfile: Path = typer.Argument(..., help="Path to save the output confusion matrix."),
    normalize: bool = typer.Option(False, "--normalize", help="Normalize the counts in the confusion matrix."),
    gpu_id: int = typer.Option(-1, "--gpu-id", "-g", help="GPU ID to use. Pass -1 to use the CPU."),
    # fmt: on
):
    if gpu_id >= 0:
        msg.info(f"Using GPU: {gpu_id}")
        spacy.prefer_gpu(gpu_id=gpu_id)
    nlp = spacy.load(model_path)

    def _get_vector(docs: Iterable[Doc]) -> Iterable[str]:
        """Get label vector from a set of documents"""
        vector = []
        for doc in docs:
            for token in doc:
                label = (
                    f"{token.ent_iob_}-{token.ent_type_}"
                    if token.ent_type_
                    else token.ent_iob_
                )
                vector.append(label)
        return vector

    # Get reference examples
    doc_bin = DocBin().from_disk(reference)
    ref_docs = list(doc_bin.get_docs(nlp.vocab))
    reference_vector = _get_vector(ref_docs)

    # Get predicted examples
    texts = [doc.text for doc in ref_docs]  # use the same text
    pred_docs = nlp.pipe(texts)
    predicted_vector = _get_vector(pred_docs)

    # Construct the confusion matrix
    labels = ["B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "O"]
    matrix = confusion_matrix(
        y_true=reference_vector, y_pred=predicted_vector, labels=labels
    )

    # Plot the confusion matrix
    if normalize:
        msg.text("Normalizing the confusion matrix")
        matrix = matrix.astype("float") / matrix.sum(axis=1)[:, np.newaxis]

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(matrix, interpolation="nearest", cmap="Greys")

    # Formatting
    ax.set(
        xticks=np.arange(matrix.shape[1]),
        yticks=np.arange(matrix.shape[0]),
        xticklabels=labels,
        yticklabels=labels,
        ylabel="Reference annotations",
        xlabel="Model predictions",
    )

    fmt = ".2f" if normalize else "d"
    threshold = matrix.max() / 2
    for rows in range(matrix.shape[0]):
        for cols in range(matrix.shape[1]):
            ax.text(
                cols,
                rows,
                format(matrix[rows, cols], fmt),
                ha="center",
                va="center",
                color="white" if matrix[rows, cols] > threshold else "black",
            )

    fig.tight_layout()
    plt.savefig(outfile, transparent=True)


if __name__ == "__main__":
    typer.run(plot_confusion_matrix)
