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


def load_wa_species() -> List[Species]:
    return _load_csv('wa')


def load_or_species() -> List[Species]:
    return _load_csv('or')


ImageTree = Dict[str, List[Image]]


@lru_cache(None)
def build_image_tree() -> ImageTree:
    tree: Dict[str, List[Image]] = {}

    wa_species = load_wa_species()
    or_species = load_or_species()

    all_common = {spec.common for spec in wa_species}
    all_common.update({spec.common for spec in or_species})
    other = set()

    for img in collection.load_images():
        if img.g_label in all_common:
            tree.setdefault(img.g_label, []).append(img)
            continue

        other.add(img.g_label)
        other_label = f'Non-RC {img.category}'.strip('s')
        tree.setdefault(other_label, []).append(img)

    found = set(tree.keys())
    missing = all_common - found

    metrics.counter('species other', len(other))
    for m in missing:
        metrics.record('missing', m)

    return tree


# PRIVATE


@lru_cache(None)
def _load_csv(fname: str) -> List[Species]:
    species = []
    csv_path = f'{config.src_root}/data/{fname}.csv'

    with open(csv_path) as fd:
        reader = csv.reader(fd)
        for row in reader:
            common, scientific, code = row
            new = Species(common, scientific, code)

            metrics.counter('species wanted')
            species.append(new)

    return species
