#!/usr/bin/python3

import hashlib
import os

from util import config


class Image:
    def __init__(self, path: str, label: str, credit: str) -> None:
        self.path = path
        self.s_label = label
        self.g_label = self._general_label()
        self.credit = credit
        if credit == 'Wei Chang':
            self.credit = 'Shou-Wei Chang'

        relative_path = path.replace(config.img_root, '')
        self.id = hashlib.md5(relative_path.encode()).hexdigest()

        self.category = relative_path.split(os.sep)[0]

    def __repr__(self) -> str:
        return f'{self.g_label} - {self.credit}'

    def _general_label(self) -> str:
        relative_path = os.path.dirname(os.path.relpath(self.path, config.img_root))
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
        }

        return conversions.get(label, label)
