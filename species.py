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


def load_washington() -> List[Species]:
    return _load_csv('wa')


def load_oregon() -> List[Species]:
    return _load_csv('or')


def load_california() -> List[Species]:
    return _load_csv('ca')


ImageTree = Dict[str, List[Image]]


@lru_cache(None)
def build_image_tree() -> ImageTree:
    tree: Dict[str, List[Image]] = {}

    wa_common = {spec.common for spec in load_washington()}
    or_common = {spec.common for spec in load_oregon()}
    ca_common = {spec.common for spec in load_california()}
    all_common = wa_common | or_common | ca_common
    other = set()

    for img in collection.load_images():
        if img.g_label in all_common:
            tree.setdefault(img.g_label, []).append(img)
            continue

        other.add(img.g_label)
        if img.g_label not in wa_common:
            other_label = f'Non-RCWA {img.category}'.strip('s')
            tree.setdefault(other_label, []).append(img)

        if img.g_label not in or_common:
            other_label = f'Non-RCOR {img.category}'.strip('s')
            tree.setdefault(other_label, []).append(img)

        if img.g_label not in ca_common:
            other_label = f'Non-RCCA {img.category}'.strip('s')
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
