from pathlib import Path
from typing import Any

import typer
import pandas as pd
from srsly import read_json
from wasabi import msg


def report(
    indir: Path = typer.Argument(..., help="Path to the evaluations directory.")
):
    """Return a table of evaluation results

    The input to `indir` must be a directory where the first-level directories are the model names,
    with JSON files from `spacy evaluate` in this file format: {task}_{dataset}.json
    """
    results = []
    for model_dir in indir.iterdir():
        if model_dir.is_dir():
            model_name = model_dir.name
            for json_file in model_dir.glob("*.json"):
                task, dataset = json_file.stem.split("_")
                data = read_json(json_file)
                results.append((model_name, task, dataset, data))

    msg.info(f"Found {len(results)} results in {indir}")

    msg.text("Parsing syntactic annotation results...")
    syn_rows = []
    for model_name, task, dataset, data in results:
        if task == "dep":
            row = {
                "model": model_name,
                "dataset": dataset,
                "token_acc": data.get("tokenizer").get("token_f"),
                "lemma_acc": data.get("trainable_lemmatizer").get("lemma_acc"),
                "tag_acc": data.get("tagger").get("tag_acc"),
                "pos_acc": data.get("morphologizer").get("pos_acc"),
                "morph_acc": data.get("morphologizer").get("morph_acc"),
                "dep_uas": data.get("parser").get("dep_uas"),
                "dep_las": data.get("parser").get("dep_las"),
            }
            syn_rows.append(row)

    def format_table(df: pd.DataFrame) -> pd.DataFrame:
        df[df.select_dtypes(include="number").columns] *= 100
        df[df.select_dtypes(include="number").columns] = df.select_dtypes(
            include="number"
        ).round(2)
        return df

    syn_df = format_table(
        pd.DataFrame(syn_rows).sort_values(by="dataset").reset_index(drop=True)
    )
    print(syn_df.to_markdown(index=False))

    msg.text("Parsing NER results...")
    ner_rows = []
    for model_name, task, dataset, data in results:
        if task == "ner":
            row = {
                "model": model_name,
                "dataset": dataset,
                "ents_p": data.get("ner").get("ents_p"),
                "ents_r": data.get("ner").get("ents_r"),
                "ents_f": data.get("ner").get("ents_f"),
            }
            ner_rows.append(row)

    ner_df = format_table(
        pd.DataFrame(ner_rows).sort_values(by="dataset").reset_index(drop=True)
    )
    print(ner_df.to_markdown(index=False))


if __name__ == "__main__":
    typer.run(report)
