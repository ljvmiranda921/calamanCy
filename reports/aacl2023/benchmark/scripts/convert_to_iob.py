from pathlib import Path

import spacy
import typer
from spacy.tokens import DocBin


def convert_to_iob(infile: Path, outfile: Path):
    nlp = spacy.blank("tl")
    doc_bin = DocBin().from_disk(infile)
    docs = list(doc_bin.get_docs(nlp.vocab))

    with open(outfile, "w") as f:
        for doc in docs:
            for token in doc:
                iob_tag = (
                    token.ent_iob_
                    if not token.ent_type_
                    else f"{token.ent_iob_}-{token.ent_type_}"
                )
                line = f"{token.text}\t{iob_tag}"
                f.write(f"{line}\n")
            f.write("\n")  # Add new line for every document


if __name__ == "__main__":
    typer.run(convert_to_iob)
