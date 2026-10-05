from pathlib import Path
from typing import Optional

import spacy
import typer
from spacy.tokens import DocBin
from wasabi import msg

SAMPLE_TEXTS = [
    "Nagpulong si Pangulong Marcos at ang DOH sa Maynila noong Lunes.",
    "Hindi ko alam kung bakit siya umalis nang maaga kahapon.",
    "Ang mga mag-aaral ay nag-aral nang mabuti para sa pagsusulit.",
    "Pumunta kami sa Quezon City para bumili ng pasalubong.",
    "Grabe, ang init today! Sana umulan na mamayang gabi.",
]


def check_alignment(
    # fmt: off
    model_names: str = typer.Argument("microsoft/mdeberta-v3-base,jhu-clsp/mmBERT-base", help="Comma-separated list of HuggingFace models to check."),
    corpus: Optional[Path] = typer.Option(None, "--corpus", help="Optional path to a .spacy file to check instead of the sample texts."),
    limit: int = typer.Option(500, "--limit", help="Maximum number of documents to check from the corpus."),
    gpu_id: int = typer.Option(-1, "--gpu-id", help="GPU ID to use. On Apple Silicon, any non-negative value uses MPS."),
    # fmt: on
):
    """Check if transformer wordpieces align with spaCy tokens"""
    if gpu_id >= 0:
        spacy.require_gpu(gpu_id)
        msg.info(f"Using GPU (gpu_id={gpu_id})")

    for model_name in model_names.split(","):
        nlp = spacy.blank("tl")
        nlp.add_pipe("transformer", config={"model": {"name": model_name}})
        nlp.initialize()

        if corpus:
            docs = list(DocBin().from_disk(corpus).get_docs(nlp.vocab))[:limit]
            texts = [doc.text for doc in docs]
        else:
            texts = SAMPLE_TEXTS

        n_tokens = 0
        unaligned = []
        for doc in nlp.pipe(texts):
            lengths = doc._.trf_data.align.lengths
            for token, length in zip(doc, lengths):
                n_tokens += 1
                if length == 0:
                    unaligned.append(token.text)

        ratio = len(unaligned) / n_tokens if n_tokens else 0.0
        msg.divider(model_name)
        msg.text(f"Checked {len(texts)} texts, {n_tokens} tokens")
        if unaligned:
            msg.warn(f"Unaligned tokens: {len(unaligned)} ({ratio:.2%})")
            msg.text(f"Examples: {unaligned[:20]}")
        else:
            msg.good("All tokens are aligned to at least one wordpiece")


if __name__ == "__main__":
    typer.run(check_alignment)
