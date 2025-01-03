#!/usr/bin/python3

import unittest

import species
from species import Species


class TestSpecies(unittest.TestCase):
    def test_load_washington_species(self) -> None:
        species_list = species.load_washington()
        self.assertNotEqual(species_list, [])

        for spec in species_list:
            self.assertNotEqual(spec.common, '')
            self.assertNotEqual(spec.scientific, '')
            self.assertNotEqual(spec.code, '')

    def test_load_oregon_species(self) -> None:
        species_list = species.load_oregon()
        self.assertNotEqual(species_list, [])

        for spec in species_list:
            self.assertNotEqual(spec.common, '')
            self.assertNotEqual(spec.scientific, '')
            self.assertNotEqual(spec.code, '')

    def test_load_california_species(self) -> None:
        species_list = species.load_california()
        self.assertNotEqual(species_list, [])

        for spec in species_list:
            self.assertNotEqual(spec.common, '')
            self.assertNotEqual(spec.scientific, '')
            self.assertNotEqual(spec.code, '')

    def test_uniqueness(self) -> None:
        species_list = species.load_washington()

        common_names = {spec.common for spec in species_list}
        self.assertEqual(len(common_names), len(species_list))

        # Treating Green and Pallid Urchins as the same
        codes = {spec.code for spec in species_list}
        self.assertEqual(len(codes), len(species_list))

        # Young of Year Rockfish, gendered species
        scientific_names = {spec.scientific for spec in species_list}
        self.assertNotEqual(len(scientific_names), len(species_list))

    def test_simple(self) -> None:
        perch = get_by_code('PIP')
        self.assertEqual(perch.common, 'Pile Perch')
        self.assertEqual(perch.scientific, 'Rhacochilus vacca')

    def test_greenling_gender(self) -> None:
        greenling = get_by_code('KGM')
        self.assertEqual(greenling.common, 'Kelp Greenling Male')
        self.assertEqual(greenling.scientific, 'Hexagrammos decagrammus')

    def test_multiple_scientific(self) -> None:
        sieve_kelp = get_by_code('SV')
        self.assertEqual(sieve_kelp.common, 'Sieve Kelp')
        self.assertEqual(sieve_kelp.scientific, 'Agarum clathratum')

    def test_parse_urchins(self) -> None:
        purple = get_by_code('PPU')
        self.assertEqual(purple.common, 'Purple Urchin')

    def test_yoy(self) -> None:
        puget_sound = get_by_code('YPS')
        self.assertEqual(puget_sound.common, 'YOY Puget Sound')

        multi = get_by_code('YBCQ')
        self.assertEqual(multi.common, 'YOY Brown/Copper/Quillback')


class TestImageTree(unittest.TestCase):
    def test_build(self) -> None:
        tree = species.build_image_tree()

        for spec, images in tree.items():
            self.assertNotEqual(images, [])

        others = (
            'Non-RCWA Fish',
            'Non-RCWA Algae',
            'Non-RCWA Invert',
            'Non-RCOR Fish',
            'Non-RCOR Algae',
            'Non-RCOR Invert',
            'Non-RCCA Fish',
            'Non-RCCA Algae',
            'Non-RCCA Invert',
        )
        for other in others:
            self.assertIn(other, tree.keys())


def get_by_code(code: str) -> Species:
    species_list = species.load_washington()
    return next((spec for spec in species_list if spec.code == code))
