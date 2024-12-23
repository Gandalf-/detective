#!/usr/bin/python3

import unittest

import species
import web
from image import Image


class TestTableBuilder(unittest.TestCase):
    def test_names(self) -> None:
        tree = species.build_image_tree()
        tree = {k: tree[k] for k in list(tree)[:3]}

        ns, ts, ps, cs = web.table_builder(tree)
        self.assertEqual(ns, ['Acid Weed', 'Broad Ribbed Kelp', 'Bull Kelp'])

    def test_category_indicies(self) -> None:
        salmon = make_image('Fish', 'Cabezon', 'John Doe')
        urchin = make_image('Inverts', 'Purple Urchin', 'Jane Doe')
        winged = make_image('Algae', 'Winged Kelp', 'John Doe')
        anemone = make_image('Inverts', 'Large Anemone', 'Jane Doe')
        oregon_only = make_image('Inverts', 'Masking Crab', 'Jane Doe')

        tree = {
            'a': [salmon],
            'b': [urchin],
            'c': [winged],
            'd': [anemone],
            'e': [oregon_only],
        }

        indicies = web.category_indices(tree)
        expected = {
            'Washington': [0, 1, 2, 3],
            'WA Fish': [0],
            'WA Inverts': [1, 3],
            'WA Algae': [2],
            'Oregon': [0, 1, 3, 4],
            'OR Fish': [0],
            'OR Inverts': [1, 3, 4],
            'OR Algae': [],
        }
        self.assertEqual(indicies, expected)


class TestDistance(unittest.TestCase):
    def test_simple(self) -> None:
        self.assertEqual(distance('Piddock Clam'), 1.0)
        self.assertEqual(distance('Hairy Triton'), 0.6)
        self.assertEqual(distance('Large Anemone'), 0.2)
        self.assertEqual(distance('Acid Weed'), 0.0)

    def test_non_rcwa(self) -> None:
        self.assertEqual(distance('Non-RC Invert'), 1.0)
        self.assertEqual(distance('Non-RC Fish'), 0.0)
        self.assertEqual(distance('Non-RC Algae'), 0.0)


def distance(other: str) -> float:
    return web.distance('Piddock Clam', other)


def make_image(category: str, label: str, credit: str) -> Image:
    new = Image('/a/b/c', '', '')
    new.category = category
    new.s_label = label
    new.g_label = label
    new.credit = credit
    return new
