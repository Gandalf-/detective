#!/usr/bin/python3

import csv
import os
import pathlib
from typing import List

data_root = str(pathlib.Path(__file__).parent.absolute()) + '/data'


class Species:
    def __init__(self, common: str, scientific: str, code: str) -> None:
        self.common = common
        self.scientific = scientific or 'None'
        self.code = code


def load_species() -> List[Species]:
    species = []

    with open(os.path.join(data_root, 'species.csv')) as fd:
        reader = csv.reader(fd)
        for row in reader:
            species.append(Species(*row))

    return species
