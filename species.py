#!/usr/bin/python3

import csv
import pathlib
from functools import lru_cache
from typing import List


class Species:
    def __init__(self, common: str, scientific: str, code: str) -> None:
        self.common = common.replace('-', ' ')

        self.scientific = scientific or 'None'
        if ',' in self.scientific:
            # XXX Arbitrary decision to only keep the first scientific name
            self.scientific = self.scientific.split(',')[0]

        self.code = code

    def __repr__(self) -> str:
        return f'{self.common} - {self.scientific} - {self.code}'


@lru_cache(None)
def load_species() -> List[Species]:
    species = []
    csv_path = str(pathlib.Path(__file__).parent.absolute()) + '/data/species.csv'

    with open(csv_path) as fd:
        reader = csv.reader(fd)
        for row in reader:
            common, scientific, code = row
            if 'YOY' in common:
                # XXX Ignore Young of Year for now
                continue

            new = Species(common, scientific, code)
            species.append(new)

    return species
