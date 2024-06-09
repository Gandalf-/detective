#!/usr/bin/python3

import os
from typing import List, Tuple

image_root = os.path.expanduser('~/Documents/Drive/Indicator Species Photos and Videos/')


class Image:
    def __init__(self, path: str, label: str, credit: str) -> None:
        self.path = path
        self.label = label
        self.credit = credit


def load(path: str) -> List[Image]:
    for path in os.listdir(path):
        if not os.path.isfile(path):
            continue

        ext = os.path.splitext(path)[1]
        if ext.lower() not in ('.jpg', '.jpeg', '.png'):
            continue

    return []


# Parsing filenames


def parse_name(filename: str) -> Tuple[str, str]:
    label, _ = os.path.splitext(filename)
    label = normalize(label)

    *name, credit = label.split('_')

    name = ' '.join(name)
    name = titlecase_to_spaces(name)
    name = strip_irrelevant(name)
    name = name.strip()

    credit = titlecase_to_spaces(credit)
    credit = handle_mc_last(credit)

    return (name, credit)


def strip_irrelevant(label: str) -> str:
    for ignore in ('Night Dive',):
        if ignore in label:
            label = label.replace(ignore, '')
    return label


def normalize(filename: str) -> str:
    """Normalize a filename to a standard format"""
    chars = []

    for c in filename:
        if c.isalpha() or c.isspace() or c == "'":
            chars.append(c)
        elif chars[-1] != '_':
            chars.append('_')

    return ''.join(chars).strip('_ ')


def handle_mc_last(name: str) -> str:
    """Handle the case where a name has a Mc prefix"""
    parts = name.split(' ')
    if len(parts) > 2 and parts[-2] == 'Mc':
        parts[-2] = 'Mc'
        return ' '.join(parts[:-2] + [f'Mc{parts[-1]}'])
    else:
        return name


def titlecase_to_spaces(x: str) -> str:
    """Convert TitleCase to Title Case"""
    chars = []

    for i, c in enumerate(x):
        if i < len(x) - 1 and c.islower() and x[i + 1].isupper():
            chars.append(c)
            chars.append(' ')
        else:
            chars.append(c)

    return ''.join(chars)
