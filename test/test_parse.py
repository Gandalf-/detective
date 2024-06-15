#!/usr/bin/python3

import unittest

import parse


class TestUtility(unittest.TestCase):
    def test_titlecase_to_spaces(self) -> None:
        self.assertEqual(parse.titlecase_to_spaces('BullKelp'), 'Bull Kelp')
        self.assertEqual(parse.titlecase_to_spaces('DavidHorwich'), 'David Horwich')

    def test_normalize(self) -> None:
        cases = [
            ('Acid Weed-1-Jackie Selbitschka', 'Acid Weed_Jackie Selbitschka'),
            ('Acid Weed-4-Jackie Selbitschka', 'Acid Weed_Jackie Selbitschka'),
            ('BullKelp_DavidHorwich', 'BullKelp_DavidHorwich'),
            ('AcidWeed.Abbott.1', 'AcidWeed_Abbott'),
            ('AcidWeed_AllisonGong2', 'AcidWeed_AllisonGong'),
            ('AcidWeed_JackieSelbitschka (1)', 'AcidWeed_JackieSelbitschka'),
        ]
        for label, expected in cases:
            self.assertEqual(parse.normalize(label), expected)


class TestParseName(unittest.TestCase):
    def test_underscore_simple(self) -> None:
        cases = [
            ('BullKelp_DavidHorwich.jpg', ('Bull Kelp', 'David Horwich')),
            ('BroadRibbedKelp_Abbott.JPG', ('Broad Ribbed Kelp', 'Abbott')),
        ]
        for filename, expected in cases:
            self.assertEqual(parse.parse_name(filename), expected)

    def test_underscore_numbered_trailing(self) -> None:
        cases = [
            ('BroadRibbedKelp_Abbott (2).JPG', ('Broad Ribbed Kelp', 'Abbott')),
            ('FiveRibbedKelp_DanAbbott1.JPG', ('Five Ribbed Kelp', 'Dan Abbott')),
        ]
        for filename, expected in cases:
            self.assertEqual(parse.parse_name(filename), expected)

    def test_trailing_letter(self) -> None:
        cases = [
            ('KelpRockfish_Abbott-a (2).JPG', ('Kelp Rockfish', 'Abbott')),
        ]
        for filename, expected in cases:
            self.assertEqual(parse.parse_name(filename), expected)

    def test_space_simple(self) -> None:
        cases = [
            ('Acid Weed-1-Jackie Selbitschka.jpeg', ('Acid Weed', 'Jackie Selbitschka')),
            ('AcidWeed_JackieSelbitschka (1).jpeg', ('Acid Weed', 'Jackie Selbitschka')),
        ]
        for filename, expected in cases:
            self.assertEqual(parse.parse_name(filename), expected)

    def test_numbered_middle(self) -> None:
        filename = 'BullKelp2_SelenaMcMillan.JPG'
        self.assertEqual(parse.parse_name(filename), ('Bull Kelp', 'Selena McMillan'))

    def test_date_middle(self) -> None:
        filename = 'BullKelpBlades_2020_08_13_SelenaMcMillan (1).JPG'
        self.assertEqual(parse.parse_name(filename), ('Bull Kelp Blades', 'Selena McMillan'))

    def test_several_names_with_underscores(self) -> None:
        filename = 'BullKelp_GiantKelp_YellowtailRockfish_BlueRockfish_DanSchwartz.jpg'
        self.assertEqual(
            parse.parse_name(filename),
            ('Bull Kelp Giant Kelp Yellowtail Rockfish Blue Rockfish', 'Dan Schwartz'),
        )

    def test_leading_number(self) -> None:
        filename = '3R.DanAbbott.jpg'
        self.assertEqual(parse.parse_name(filename), ('R', 'Dan Abbott'))

    def test_unrelated_underscores(self) -> None:
        filename = 'Seagrass_2020_08_07_SelenaMcMillan (1).JPG'
        self.assertEqual(parse.parse_name(filename), ('Seagrass', 'Selena McMillan'))

    def test_unrelated_label(self) -> None:
        filename = 'Blacksmith_2022_06_02_NightDive_SelenaMcMillan (1).JPG'
        self.assertEqual(parse.parse_name(filename), ('Blacksmith', 'Selena McMillan'))

    def test_scientific_name(self) -> None:
        cases = [
            (
                'Caulerpa taxifolia_RachelWoodfield (1).jpg',
                ('Caulerpa taxifolia', 'Rachel Woodfield'),
            ),
            ('Hedophyllum sessile2-HilaryHayford.jpg', ('Hedophyllum sessile', 'Hilary Hayford')),
            ('H.nigripes.Abbott (2).JPG', ('H nigripes', 'Abbott')),
        ]
        for filename, expected in cases:
            self.assertEqual(parse.parse_name(filename), expected)

    def test_mixed_casing(self) -> None:
        filename = 'Giant kelp 5-MexCal.JPG'
        self.assertEqual(parse.parse_name(filename), ('Giant kelp', 'Mex Cal'))

    def test_apostrophe(self) -> None:
        filename = "GiantKelp_TomO'Leary.jpg"
        self.assertEqual(parse.parse_name(filename), ('Giant Kelp', "Tom O'Leary"))

    def test_yoy_black_yellowtail(self) -> None:
        filename = 'BlackRockfishYOY_BenTroxell.jpg'
        self.assertEqual(parse.parse_name(filename), ('YOY Black/Yellowtail', 'Ben Troxell'))

        filename = 'YellowtailRockfishYOY2-TabithaJM.jpg'
        self.assertEqual(parse.parse_name(filename), ('YOY Black/Yellowtail', 'Tabitha JM'))

    def test_yoy_blue_deacon(self) -> None:
        filename = 'BlueRockfishYOY_ChrisHoneyman (2).jpg'
        self.assertEqual(parse.parse_name(filename), ('YOY Blue/Deacon', 'Chris Honeyman'))
        # No Deacon YOY's

    def test_yoy_bocaccio(self) -> None:
        filename = 'BocaccioYOY_AndrewHarmer.jpg'
        self.assertEqual(parse.parse_name(filename), ('YOY Bocaccio', 'Andrew Harmer'))

    def test_yoy_brown_copper_quillback(self) -> None:
        filename = 'BrownRockfishYOY-TabithaJM.jpg'
        self.assertEqual(parse.parse_name(filename), ('YOY Brown/Copper/Quillback', 'Tabitha JM'))

        filename = 'CopperRockfishYOY3-TabithaJM.jpg'
        self.assertEqual(parse.parse_name(filename), ('YOY Brown/Copper/Quillback', 'Tabitha JM'))

        filename = 'QuillbackRockfishYOY.LauraTesler.jpg'
        self.assertEqual(parse.parse_name(filename), ('YOY Brown/Copper/Quillback', 'Laura Tesler'))

    def test_yoy_canary(self) -> None:
        filename = 'CanaryRockfishYOY-AdamObaza.png'
        self.assertEqual(parse.parse_name(filename), ('YOY Canary', 'Adam Obaza'))

    def test_yoy_puget_sound(self) -> None:
        filename = 'PugetSoundRockfishYOY4-TabithaJM (1).jpg'
        self.assertEqual(parse.parse_name(filename), ('YOY Puget Sound', 'Tabitha JM'))

    def test_yoy_vermillion(self) -> None:
        filename = 'VermilionRockfishYOY_SelenaMcMillan (5).JPG'
        self.assertEqual(parse.parse_name(filename), ('YOY Vermilion', 'Selena McMillan'))

    def test_yoy_yelloweye(self) -> None:
        filename = 'YelloweyeRockfishYOY-LauraTesler.jpg'
        self.assertEqual(parse.parse_name(filename), ('YOY Yelloweye', 'Laura Tesler'))
