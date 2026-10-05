from pathlib import Path
from typing import Optional

import srsly
import typer
from datasets import load_dataset
from wasabi import msg

# FineWeb-2 configs for languages in the Philippines with at least ~1k documents
FINEWEB2_PH_LANGUAGES = [
    "fil_Latn",  # Filipino (2,349,050 docs)
    "ceb_Latn",  # Cebuano (204,636 docs)
    "hil_Latn",  # Hiligaynon (43,810 docs)
    "ilo_Latn",  # Ilocano (21,304 docs)
    "bcl_Latn",  # Central Bikol (8,822 docs)
    "pag_Latn",  # Pangasinan (2,712 docs)
    "war_Latn",  # Waray (2,223 docs)
    "pam_Latn",  # Kapampangan (2,005 docs)
    "cbk_Latn",  # Chavacano (1,872 docs)
    "ify_Latn",  # Keley-I Kallahan (1,364 docs)
    "mbb_Latn",  # Western Bukidnon Manobo (1,207 docs)
    "krj_Latn",  # Kinaray-a (1,098 docs)
]


def download_pretraining_data(
    # fmt: off
    output_dir: Path = typer.Argument(..., help="Directory to save the JSONL files for each source."),
    text_output: Optional[Path] = typer.Option(None, "--text-output", help="If set, also writes all documents as plain text (one document per line) for training floret vectors."),
    languages: str = typer.Option(",".join(FINEWEB2_PH_LANGUAGES), "--languages", help="Comma-separated list of FineWeb-2 configs to download."),
    include_halohalo: bool = typer.Option(True, "--include-halohalo/--no-halohalo", help="Whether to include the sapinsapin/halohalo dataset."),
    max_docs: Optional[int] = typer.Option(None, "--max-docs", help="If set, limits the number of documents per source (useful for testing)."),
    # fmt: on
):
    """Download pretraining text from FineWeb-2 and halohalo

    Each source is saved as JSONL with the fields `id`, `text`, `language`, and
    `source`. The JSONL format can be used directly with `spacy pretrain`.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    sources = [("HuggingFaceFW/fineweb-2", lang) for lang in languages.split(",")]
    if include_halohalo:
        sources.append(("sapinsapin/halohalo", None))

    jsonl_paths = []
    for dataset, config in sources:
        name = f"fineweb2-{config}" if config else dataset.split("/")[-1]
        outfile = output_dir / f"{name}.jsonl"
        if outfile.exists():
            msg.info(f"Found existing {outfile}, skipping download")
            jsonl_paths.append(outfile)
            continue

        msg.info(f"Downloading {dataset} ({config or 'default'})")
        ds = load_dataset(dataset, name=config, split="train", streaming=True)
        if max_docs:
            ds = ds.take(max_docs)

        def format_doc(eg):
            return {
                "id": eg["id"],
                "text": eg["text"],
                "language": config.split("_")[0] if config else eg["language"],
                "source": name,
            }

        srsly.write_jsonl(outfile, (format_doc(eg) for eg in ds))
        msg.good(f"Saved {name} to {outfile}")
        jsonl_paths.append(outfile)

    if text_output:
        n_docs = 0
        with text_output.open("w", encoding="utf-8") as f:
            for jsonl_path in jsonl_paths:
                for eg in srsly.read_jsonl(jsonl_path):
                    f.write(" ".join(eg["text"].split()) + "\n")
                    n_docs += 1
        msg.good(f"Saved {n_docs} documents as plain text to {text_output}")


if __name__ == "__main__":
    typer.run(download_pretraining_data)
