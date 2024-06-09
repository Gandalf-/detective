#!/usr/bin/python3

import os
from typing import List, Tuple


class Image:
    def __init__(self, path: str, label: str, credit: str) -> None:
        self.path = path
        self.s_label = label
        self.g_label = self._general_label()
        self.credit = credit

    def __repr__(self) -> str:
        return f'{self.g_label} - {self.credit}'

    def _general_label(self) -> str:
        label = os.path.basename(os.path.dirname(self.path))
        label = label.split('(')[0].strip()
        return label


def make_root(path: str) -> str:
    image_root = os.path.expanduser('~/Documents/Drive/Indicator Species Photos and Videos/')
    return os.path.join(image_root, path)


def load_category(category: str) -> List[Image]:
    images = []

    for root in os.listdir(category):
        root_path = os.path.join(category, root)

        if not os.path.isdir(root_path):
            continue

        if root in ('Unidentified', 'Other Mixed'):
            continue

        images.extend(load_root(root_path))

    return images


def load_root(root: str) -> List[Image]:
    images: List[Image] = []

    for filename in os.listdir(root):
        path = os.path.join(root, filename)

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


# Parsing filenames


def parse_name(filename: str) -> Tuple[str, str]:
    label, _ = os.path.splitext(filename)
    label = normalize(label)

    *names, credit = label.split('_')
    name, credit = handle_letter_suffix(names, credit)

    name = titlecase_to_spaces(name)
    name = strip_irrelevant(name)
    name = name.strip()

    credit = titlecase_to_spaces(credit)
    credit = handle_mc_last(credit)

    return (name, credit)


def handle_letter_suffix(names: List[str], credit: str) -> Tuple[str, str]:
    if len(credit) == 1 and credit.isalpha():
        credit = names[-1]
        names = names[:-1]

    name = ' '.join(names)
    return (name, credit)


def strip_irrelevant(label: str) -> str:
    for ignore in ('Night Dive',):
        if ignore in label:
            label = label.replace(ignore, '')
    return label


def normalize(filename: str) -> str:
    """Normalize a filename to a standard format"""
    chars = []

    for i, c in enumerate(filename):
        if c.isalpha() or c.isspace() or c == "'":
            chars.append(c)
        elif i > 0 and chars[-1] != '_':
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
