#!/usr/bin/python3

import csv
from functools import lru_cache
from typing import Dict, List

import collection
from image import Image
from util import config
from util.metrics import metrics


class Species:
    def __init__(self, common: str, scientific: str, code: str) -> None:
        common = common.replace('-', ' ')
        common = common.replace('Sea Urchin', 'Urchin')
        self.common = common

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
    csv_path = f'{config.src_root}/data/species.csv'

    with open(csv_path) as fd:
        reader = csv.reader(fd)
        for row in reader:
            common, scientific, code = row
            if 'YOY' in common:
                # XXX Ignore Young of Year for now
                continue

            new = Species(common, scientific, code)

            metrics.counter('species wanted')
            species.append(new)

    return species


ImageTree = Dict[str, List[Image]]


@lru_cache(None)
def build_image_tree() -> ImageTree:
    tree: Dict[str, List[Image]] = {}

    species = load_species()
    all_common = {spec.common for spec in species}
    other = set()

    for img in collection.load_images():
        if img.g_label in all_common:
            tree.setdefault(img.g_label, []).append(img)
            continue

        other.add(img.g_label)
        other_label = f'Non-RCWA {img.category}'.strip('s')
        tree.setdefault(other_label, []).append(img)

    found = set(tree.keys())
    missing = all_common - found

    metrics.counter('species other', len(other))
    for m in missing:
        metrics.record('missing', m)

    return tree
