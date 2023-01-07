from mmap import mmap
from pathlib import Path

import srsly
import typer
from tqdm import tqdm
from wasabi import msg

Arg = typer.Argument


def prepare_raw_text(
    # fmt: off
    input_filepath: Path = Arg(..., exists=True, help="Input raw text file to convert to JSONL."),
    output_filepath: Path = Arg(..., exists=False, help="Output filepath to save the JSONL file")
    # fmt: on
):
    """Convert a raw text file into JSONL for pretraining

    This command follows the spaCy convention of creating a JSONL file
    where each line is a dictionary with the 'text' key:

        {'text': 'My text ...'}
        {'text': 'My text ...'}
        {'text': 'My text ...'}
    """

    def _get_num_lines(fp: Path) -> int:
        _fp = fp.open("r+")
        buf = mmap(_fp.fileno(), 0)
        lines = 0
        while buf.readline():
            lines += 1
        return lines

    lines = []
    with input_filepath.open("r") as f:
        for line in tqdm(f, total=_get_num_lines(input_filepath)):
            lines.append({"text": line.rstrip()})

    msg.info(f"Found {len(lines)} documents")
    srsly.write_jsonl(output_filepath, lines)
    msg.good(f"Saved to {output_filepath}")


if __name__ == "__main__":
    typer.run(prepare_raw_text)
