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
        salmon = make_image('Fish', 'Salmon', 'John Doe')
        urchin = make_image('Inverts', 'Urchin', 'Jane Doe')
        winged = make_image('Algae', 'Winged Kelp', 'John Doe')
        anemone = make_image('Inverts', 'Anemone', 'Jane Doe')
        tree = {
            'a': [salmon],
            'b': [urchin],
            'c': [winged],
            'd': [anemone],
        }

        indicies = web.category_indices(tree)
        expected = {
            'Washington': [0, 1, 2, 3],
            'Fish': [0],
            'Inverts': [1, 3],
            'Algae': [2],
        }
        self.assertEqual(indicies, expected)


def make_image(category: str, label: str, credit: str) -> Image:
    new = Image('/a/b/c', '', '')
    new.category = category
    new.s_label = label
    new.g_label = label
    new.credit = credit
    return new
