"""Get nearest language given a language code using a WALS-reliant metric

This script attempts to give you the nearest language for a given target using
the typological features found in WALS. A lot of these methods are based from
the work, Cross-lingual parser selection for low-resource languages, by Zeljko
Agic. Their work actually proposes a more comprehensive metric, but I think that
a simpler WALS-reliant approach should work.

The code was adapted from the original repository:
https://github.com/zeljkoagic/freasy
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

import typer
import scipy.spatial.distance as dist

DEFAULT_WALS_PATH = Path("assets/wals/language.csv")
DEFAULT_ISO_PATH = Path("assets/wals/iso_mapping.txt")

def get_nearest_language(
    # fmt: off
    lang: str = typer.Argument(..., help="ISO language code for the target language."),
    source: Path = typer.Option(DEFAULT_WALS_PATH, "-s", "--source", help="Path to the CSV file containing the WALS feature table."),
    iso_mapping: Path = typer.Option(DEFAULT_ISO_PATH, "-i", "--iso", help="Path to the TXT file containing the ISO mapping."),
    source_langs: str = typer.Option(None, "-s", "--source", help="Comma-separated list of ISO 639-2 language codes to restrict the search space. If None, will search all languages."),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Print out additional information."),
    # fmt: on
):
    # Load the WALS data and the ISO mappings
    wals_data = _read_wals_csv(source)
    iso2to3, iso3to2 = _read_iso_mappings(iso_mapping)

    target_names = iso2to3.get(lang)
    search_space = list(iso2to3.keys()) if not source_langs else source_langs.split(",")
    closest_source = None
    min_distance = sys.float_info.max
    source_distrib = []

    # This one is a line by line copy of the original implementation
    # c.f. https://github.com/zeljkoagic/freasy/blob/5db0455f7b97c8057e824b84c3b067bebd32efb0/src/freasy/wals.py#L42
    for source_lang in search_space:
        source_names = iso2to3[source_lang]
        for target_name in target_names:
            for source_name in source_names:
                target_vectors = wals_data[target_name]
                source_vectors = wals_data[source_name]

                min_distance_for_source = sys.float_info.max
                for target_vector in target_vectors:
                    for source_vector in source_vectors:
                        assert len(target_vector) == len(source_vector), f"Vectors must be equal in length! {target_vector}, {source_vector}"

                        # Some languages have incomplete vectors, and we compare only the non-empty fields
                        fair_tv = []
                        fair_sv = []
                        for i in range(len(target_vector)):
                            if target_vector[i] and source_vector[i]:
                                fair_tv.append(target_vector[i])
                                fair_sv.append(source_vector[i])

                        distance = dist.hamming(fair_tv, fair_sv)

                        if distance < min_distance:
                            min_distance = distance
                            closest_source = source_name
                        if distance < min_distance_for_source:
                            min_distance_for_source = distance

                if min_distance_for_source != sys.float_info.max:
                    source_distrib.append((iso3to2[source_name], min_distance_for_source))
    breakpoint()



def _read_wals_csv(infile: Path) -> Dict[str, List[Any]]:
    """Load the WALS database CSV"""
    with open(infile) as f:
        reader = csv.reader(f)
        wals_data = {row[1]: row for row in reader if row[1]}
    return wals_data

def _read_iso_mappings(infile: Path) -> Tuple[Dict[str, List], Dict[str, str]]:
    """Load the ISO 639-2/3 mappings"""
    iso2to3 = defaultdict(list)
    iso3to2 = defaultdict()
    with open(infile) as f:
        for line in f:
            line = line.strip()
            if line:
                iso3, iso2 = line.split()
                iso2to3[iso2].append(iso3)
                iso3to2[iso3] = iso2
    return iso2to3, iso3to2

if __name__ == "__main__":
    typer.run(get_nearest_language)
