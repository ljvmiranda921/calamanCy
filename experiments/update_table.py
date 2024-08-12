from pathlib import Path

import pandas as pd
import typer
from srsly import read_yaml

DEFAULT_README_PATH = Path("./README.md")
README_TEMPLATE = """# Experiments

This directory contains several experiments and benchmarks for developing calamanCy. 
To generate the table below, run `python update_table.py` while inside this directory.

{table}
"""


def main(readme_path: Path = DEFAULT_README_PATH):
    """Update the contents table in the README"""

    root = Path(__file__).parent
    meta_files = sorted(root.glob("*/project.yml"))

    metadata = []
    for fp in meta_files:
        name = fp.parent.name
        url = (
            f"https://github.com/ljvmiranda921/calamanCy/tree/master/experiments/{name}"
        )
        meta = read_yaml(fp)
        metadata.append({"Path": f"[{name}]({url})", "Title": meta.get("title")})

    table = pd.DataFrame(metadata).to_markdown(index=False)
    readme = README_TEMPLATE.format(table=table)
    with readme_path.open("w") as readme_file:
        readme_file.write(readme)


if __name__ == "__main__":
    typer.run(main)
