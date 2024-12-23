#!/usr/bin/python3

import unittest

import taxonomy
from species import load_wa_species, load_or_species


class TestTaxonomy(unittest.TestCase):
    def test_load_taxonomy(self) -> None:
        tx = taxonomy.load_taxonomy()
        self.assertNotEqual(tx, {})
        self.assertIn('Copper Rockfish', tx)

    def test_all_wa_species_have_taxia(self) -> None:
        tx = taxonomy.load_taxonomy()
        species_list = load_wa_species()

        for spec in species_list:
            self.assertIn(spec.common, tx.keys(), f'{spec.common} not in taxonomy')

    def test_all_or_species_have_taxia(self) -> None:
        tx = taxonomy.load_taxonomy()
        species_list = load_or_species()

        for spec in species_list:
            self.assertIn(spec.common, tx.keys(), f'{spec.common} not in taxonomy')
