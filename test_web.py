#!/usr/bin/python3

import unittest

import species
import web


class TestTableBuilder(unittest.TestCase):
    def test_names(self) -> None:
        tree = species.build_image_tree()
        tree = {k: tree[k] for k in list(tree)[:3]}

        ns, ts, ss, ds = web.table_builder(tree)
        self.assertEqual(ns, ['Bull Kelp', 'Five ribbed Kelp', 'Sieve Kelp'])

        for images in ts:
            self.assertLessEqual(len(images), 20)


if __name__ == '__main__':
    unittest.main()
