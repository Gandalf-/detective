#!/usr/bin/python3

import os
from functools import lru_cache
from typing import List

import parse
import quality
from image import Image
from util import config
from util.metrics import metrics


def load_images() -> List[Image]:
    images: List[Image] = []

    for category in ('Algae', 'Fish', 'Inverts'):
        path = make_root(category)
        images.extend(load_category(path))

    return images


# PRIVATE


def make_root(path: str) -> str:
    return os.path.join(config.img_root, path)


def load_category(category: str) -> List[Image]:
    images = []

    for root in sorted(os.listdir(category)):
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

    for filename in sorted(os.listdir(root)):
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
            label, credit = parse.parse_name(filename)
        except IndexError:
            print(f'Error parsing {path}')
            continue

        image = Image(path, label, credit)
        if quality.unacceptable(image):
            metrics.counter('images low quality')
            continue

        metrics.counter('images parsed')
        images.append(image)

    return images
