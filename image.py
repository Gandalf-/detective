#!/usr/bin/python3

import hashlib
import os

from util import config


class Image:
    def __init__(self, path: str, label: str, credit: str) -> None:
        self.path = path
        self.s_label = label
        if 'YOY ' in label:
            self.g_label = label
        else:
            self.g_label = _label_from_path(path)

        self.credit = credit
        if credit == 'Wei Chang':
            self.credit = 'Shou-Wei Chang'

        if self.g_label == 'Treefish':
            if 'juvenile' in path.lower():
                self.g_label = 'Treefish Juvenile'
            else:
                self.g_label = 'Treefish Adult'

        relative_path = path.replace(config.img_root, '')
        self.id = hashlib.md5(relative_path.encode()).hexdigest()

        self.category = relative_path.split(os.sep)[0]

    def __repr__(self) -> str:
        return f'{self.g_label} - {self.credit}'


def _label_from_path(path: str) -> str:
    relative_path = os.path.dirname(os.path.relpath(path, config.img_root))
    label = relative_path.split(os.sep, 1)[1].replace('/', ' ')
    label = label.split('(')[0].strip()

    conversions = {
        'Anemones': 'Large Anemone',
        'Pterygophora': 'Woody Kelp',
        'Sargassum horneri': 'Horn Weed',
        'Laminaria setchelii': 'Torn Kelp',
        'Sargassum muticum': 'Wire Weed',
        'Three-ribbed Kelp': 'Three ribbed Kelp',
        'Five-ribbed Kelp': 'Five ribbed Kelp',
        "Stimpson's Sun Star": 'Blue Striped Sun Star',
        'False Ochre Star': 'Mottled Star',
        'Hornshark': 'Horn Shark',
        'Laminaria farlowii': 'Oar Kelp',
        'Undaria': 'Wakame',
        'Golden Gorgonian': 'California Golden/Brown Gorgonian',
        'Brown Gorgonian': 'California Golden/Brown Gorgonian',
        'Caulerpa taxifolia': 'Running Weed',
        'Caulerpa prolifera': 'Running Weed',
    }

    return conversions.get(label, label)
