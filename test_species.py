#!/usr/bin/python3

import unittest

import species
from species import Species


class TestSpecies(unittest.TestCase):
    def test_load_species(self) -> None:
        species_list = species.load_species()
        self.assertNotEqual(species_list, [])

        for spec in species_list:
            self.assertNotEqual(spec.common, '')
            self.assertNotEqual(spec.scientific, '')
            self.assertNotEqual(spec.code, '')

    def test_uniqueness(self) -> None:
        species_list = species.load_species()

        common_names = {spec.common for spec in species_list}
        self.assertEqual(len(common_names), len(species_list))

        # Young of Year Rockfish, gendered species
        scientific_names = {spec.scientific for spec in species_list}
        self.assertNotEqual(len(scientific_names), len(species_list))

        # Green/Pallid Sea Urchin
        codes = {spec.code for spec in species_list}
        self.assertNotEqual(len(codes), len(species_list))

    def test_simple(self) -> None:
        perch = get_by_code('PIP')
        self.assertEqual(perch.common, 'Pile Perch')
        self.assertEqual(perch.scientific, 'Rhacochilus vacca')

    @unittest.skip('Needs image updates')
    def test_greenling_gender(self) -> None:
        pass

    def test_multiple_scientific(self) -> None:
        sieve_kelp = get_by_code('SV')
        self.assertEqual(sieve_kelp.common, 'Sieve Kelp')
        self.assertEqual(sieve_kelp.scientific, 'Agarum clathratum')


def get_by_code(code: str) -> Species:
    species_list = species.load_species()
    return next((spec for spec in species_list if spec.code == code))


if __name__ == '__main__':
    unittest.main()
