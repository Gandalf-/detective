#!/usr/bin/python3

import unittest

import species
import web


class TestTableBuilder(unittest.TestCase):
    def test_names(self) -> None:
        tree = species.build_image_tree()
        tree = {k: tree[k] for k in list(tree)[:3]}

        ns, ts, ss, ps, cs = web.table_builder(tree)
        self.assertEqual(ns, ['Acid Weed', 'Broad Ribbed Kelp', 'Bull Kelp'])
