#!/usr/bin/python3

import os
import unittest

import image


class TestUtility(unittest.TestCase):
    def test_image_root(self):
        exists = os.path.exists(image.image_root)
        assert exists

    def test_titlecase_to_spaces(self):
        self.assertEqual(image.titlecase_to_spaces('BullKelp'), 'Bull Kelp')
        self.assertEqual(image.titlecase_to_spaces('DavidHorwich'), 'David Horwich')

    def test_normalize(self):
        cases = [
            ('Acid Weed-1-Jackie Selbitschka', 'Acid Weed_Jackie Selbitschka'),
            ('Acid Weed-4-Jackie Selbitschka', 'Acid Weed_Jackie Selbitschka'),
            ('BullKelp_DavidHorwich', 'BullKelp_DavidHorwich'),
            ('AcidWeed.Abbott.1', 'AcidWeed_Abbott'),
            ('AcidWeed_AllisonGong2', 'AcidWeed_AllisonGong'),
            ('AcidWeed_JackieSelbitschka (1)', 'AcidWeed_JackieSelbitschka'),
        ]
        for label, expected in cases:
            self.assertEqual(image.normalize(label), expected)


class TestParseName(unittest.TestCase):
    def test_underscore_simple(self):
        cases = [
            ('BullKelp_DavidHorwich.jpg', ('Bull Kelp', 'David Horwich')),
            ('BroadRibbedKelp_Abbott.JPG', ('Broad Ribbed Kelp', 'Abbott')),
        ]
        for filename, expected in cases:
            self.assertEqual(image.parse_name(filename), expected)

    def test_underscore_numbered_trailing(self):
        cases = [
            ('BroadRibbedKelp_Abbott (2).JPG', ('Broad Ribbed Kelp', 'Abbott')),
            ('FiveRibbedKelp_DanAbbott1.JPG', ('Five Ribbed Kelp', 'Dan Abbott')),
        ]
        for filename, expected in cases:
            self.assertEqual(image.parse_name(filename), expected)

    def test_space_simple(self):
        cases = [
            ('Acid Weed-1-Jackie Selbitschka.jpeg', ('Acid Weed', 'Jackie Selbitschka')),
            ('AcidWeed_JackieSelbitschka (1).jpeg', ('Acid Weed', 'Jackie Selbitschka')),
        ]
        for filename, expected in cases:
            self.assertEqual(image.parse_name(filename), expected)

    def test_numbered_middle(self):
        filename = 'BullKelp2_SelenaMcMillan.JPG'
        self.assertEqual(image.parse_name(filename), ('Bull Kelp', 'Selena McMillan'))

    def test_date_middle(self):
        filename = 'BullKelpBlades_2020_08_13_SelenaMcMillan (1).JPG'
        self.assertEqual(image.parse_name(filename), ('Bull Kelp Blades', 'Selena McMillan'))

    def test_several_names_with_underscores(self):
        filename = 'BullKelp_GiantKelp_YellowtailRockfish_BlueRockfish_DanSchwartz.jpg'
        self.assertEqual(
            image.parse_name(filename),
            ('Bull Kelp Giant Kelp Yellowtail Rockfish Blue Rockfish', 'Dan Schwartz'),
        )

    def test_unrelated_underscores(self):
        filename = 'Seagrass_2020_08_07_SelenaMcMillan (1).JPG'
        self.assertEqual(image.parse_name(filename), ('Seagrass', 'Selena McMillan'))

    def test_unrelated_label(self):
        filename = 'Blacksmith_2022_06_02_NightDive_SelenaMcMillan (1).JPG'
        self.assertEqual(image.parse_name(filename), ('Blacksmith', 'Selena McMillan'))

    def test_scientific_name(self):
        cases = [
            (
                'Caulerpa taxifolia_RachelWoodfield (1).jpg',
                ('Caulerpa taxifolia', 'Rachel Woodfield'),
            ),
            ('Hedophyllum sessile2-HilaryHayford.jpg', ('Hedophyllum sessile', 'Hilary Hayford')),
            ('H.nigripes.Abbott (2).JPG', ('H nigripes', 'Abbott')),
        ]
        for filename, expected in cases:
            self.assertEqual(image.parse_name(filename), expected)

    def test_mixed_casing(self):
        filename = 'Giant kelp 5-MexCal.JPG'
        self.assertEqual(image.parse_name(filename), ('Giant kelp', 'Mex Cal'))

    def test_apostrophe(self):
        filename = "GiantKelp_TomO'Leary.jpg"
        self.assertEqual(image.parse_name(filename), ('Giant Kelp', "Tom O'Leary"))


if __name__ == '__main__':
    unittest.main()
