#!/usr/bin/python3

import hashlib
import os
from functools import lru_cache
from typing import List

from parse import parse_name

image_root = os.path.expanduser('~/Documents/Drive/Indicator Species Photos and Videos/')


class Image:
    def __init__(self, path: str, label: str, credit: str) -> None:
        self.path = path
        self.s_label = label
        self.g_label = self._general_label()
        self.credit = credit

        relative_path = path.replace(image_root, '')
        self.id = hashlib.md5(relative_path.encode()).hexdigest()

    def __repr__(self) -> str:
        return f'{self.g_label} - {self.credit}'

    def _general_label(self) -> str:
        relative_path = os.path.dirname(os.path.relpath(self.path, image_root))
        label = relative_path.split(os.sep, 1)[1].replace('/', ' ')
        label = label.split('(')[0].strip()
        return label


def load_everything() -> List[Image]:
    images: List[Image] = []

    for category in ('Algae', 'Fish', 'Inverts'):
        path = make_root(category)
        images.extend(load_category(path))

    return images


# PRIVATE


def make_root(path: str) -> str:
    return os.path.join(image_root, path)


def load_category(category: str) -> List[Image]:
    images = []

    for root in os.listdir(category):
        root_path = os.path.join(category, root)

        if not os.path.isdir(root_path):
            continue

        if root in ('Unidentified', 'Other Mixed', 'YOY'):
            continue

        images.extend(load_root(root_path))

    return images


@lru_cache(None)
def load_root(root: str) -> List[Image]:
    images: List[Image] = []

    for filename in os.listdir(root):
        path = os.path.join(root, filename)

        if path.endswith('Undaria.Dan Abbott'):
            # XXX completely different format
            continue

        if os.path.isdir(path):
            sub_path = os.path.join(root, filename)
            images.extend(load_root(sub_path))

        if not os.path.isfile(path):
            continue

        ext = os.path.splitext(path)[1]
        if ext.lower() not in ('.jpg', '.jpeg', '.png'):
            continue

        try:
            label, credit = parse_name(filename)
        except IndexError:
            print(f'Error parsing {path}')
            continue

        image = Image(path, label, credit)
        images.append(image)

    return images
