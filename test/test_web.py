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
        sculpin = make_image('Fish', 'Cabezon', 'John Doe')
        urchin = make_image('Inverts', 'Purple Urchin', 'Jane Doe')
        winged = make_image('Algae', 'Winged Kelp', 'John Doe')
        anemone = make_image('Inverts', 'Large Anemone', 'Jane Doe')
        oregon_fish = make_image('Fish', 'Black and Yellow Rockfish', 'Jane Doe')
        oregon_abalone = make_image('Inverts', 'Red Abalone', 'Jane Doe')
        california_algae = make_image('Algae', 'Oar Kelp', 'John Doe')

        tree = {
            'A': [sculpin],
            'B': [urchin],
            'C': [winged],
            'D': [anemone],
            'E': [oregon_fish],
            'Non-RCWA Invert': [oregon_abalone],
            'O': [california_algae],
        }

        indicies = web.category_indices(tree)
        expected = {
            'Washington': [0, 1, 2, 3],
            'WA Fish': [0],
            'WA Inverts': [1, 3, 5],
            'WA Algae': [2],
            'Oregon': [0, 1, 3, 4, 5],
            'OR Fish': [0, 4],
            'OR Inverts': [1, 3, 5],
            'OR Algae': [],
            'California': [0, 1, 3, 4, 5, 6],
            'CA Fish': [0, 4],
            'CA Inverts': [1, 3, 5],
            'CA Algae': [6],
        }

        self.maxDiff = None
        self.assertEqual(indicies, expected)


class TestDistance(unittest.TestCase):
    def test_simple(self) -> None:
        self.assertEqual(distance('Piddock Clam'), 1.0)
        self.assertEqual(distance('Hairy Triton'), 2 / 3)
        self.assertEqual(distance('Large Anemone'), 0.2)
        self.assertEqual(distance('Acid Weed'), 0.0)

    def test_non_rcwa(self) -> None:
        self.assertEqual(distance('Non-RCWA Invert'), 1.0)
        self.assertEqual(distance('Non-RCWA Fish'), 0.0)
        self.assertEqual(distance('Non-RCWA Algae'), 0.0)

    def test_non_rcor(self) -> None:
        self.assertEqual(distance('Non-RCOR Invert'), 1.0)
        self.assertEqual(distance('Non-RCOR Fish'), 0.0)
        self.assertEqual(distance('Non-RCOR Algae'), 0.0)


def distance(other: str) -> float:
    return web.distance('Piddock Clam', other)


def make_image(category: str, label: str, credit: str) -> Image:
    new = Image('/a/b/c', '', '')
    new.category = category
    new.s_label = label
    new.g_label = label
    new.credit = credit
    return new
