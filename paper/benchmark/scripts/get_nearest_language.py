"""Get nearest language given a language code using a WALS-reliant metric

This script attempts to give you the nearest language for a given target using
the typological features found in WALS. A lot of these methods are based from
the work, Cross-lingual parser selection for low-resource languages, by Zeljko
Agic. Their work actually proposes a more comprehensive metric, but I think that
a simpler WALS-reliant approach should work.

The code was adapted from the original repository:
https://github.com/zeljkoagic/freasy
"""

from pathlib import Path

import typer

DEFAULT_WALS_PATH = Path("assets/wals/language.csv")
DEFAULT_ISO_PATH = Path("assets/wals/iso_mapping.txt")

def get_nearest_language(
    # fmt: off
    lang: str = typer.Argument(..., help="ISO language code for the target language."),
    source: Path = typer.Option(DEFAULT_WALS_PATH, "-s", "--source", help="Path to the CSV file containing the WALS feature table."),
    iso_mapping: Path = typer.Option(DEFAULT_ISO_PATH, "-i", "--iso", help="Path to the TXT file containing the ISO mapping."),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Print out additional information."),
    # fmt: on
):
    pass


if __name__ == "__main__":
    typer.run(get_nearest_language)
