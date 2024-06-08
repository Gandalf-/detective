#!/usr/bin/python3

import os

image_root = os.path.expanduser('~/Documents/Drive/Indicator Species Photos and Videos/')


class Image:
    def __init__(self, path: str, credit: str) -> None:
        self.path = path
        self.credit = credit


def load(path: str) -> [Image]:
    return []


def parse_name(filename: str) -> (str, str):
    label, _ = os.path.splitext(filename)
    name, credit = label.split('_')

    name = titlecase_to_spaces(name)
    credit = titlecase_to_spaces(credit)

    return (name, credit)


def titlecase_to_spaces(x: str) -> str:
    """Convert TitleCase to Title Case"""
    for i, c in enumerate(x):
        if c.isupper() and i > 0:
            x = x[:i] + ' ' + x[i:]

    return x
