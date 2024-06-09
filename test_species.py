#!/usr/bin/python3

import unittest

import species


class TestSpecies(unittest.TestCase):
    def test_load_species(self) -> None:
        species_list = species.load_species()
        self.assertNotEqual(species_list, [])

        for spec in species_list:
            self.assertNotEqual(spec.common, '')
            self.assertNotEqual(spec.scientific, '')
            self.assertNotEqual(spec.code, '')


if __name__ == '__main__':
    unittest.main()
