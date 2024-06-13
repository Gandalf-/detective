#!/usr/bin/python3

import os
import unittest

import collection


class TestLoad(unittest.TestCase):
    def test_load_bull_kelp(self) -> None:
        bull_kelp_root = collection.make_root('Algae/Bull Kelp')
        images = collection.load_root(bull_kelp_root)
        self.assertNotEqual(images, [])

        for img in images:
            self.assertTrue(os.path.exists(img.path))
            self.assertNotEqual(img.s_label, '')
            self.assertNotEqual(img.credit, '')

            self.assertIn('Bull Kelp', img.s_label)
            self.assertEqual(img.g_label, 'Bull Kelp')

    def test_load_acid_weed(self) -> None:
        acid_weed_root = collection.make_root('Algae/Acid Weed (Desmarestia ligulata)')
        images = collection.load_root(acid_weed_root)
        self.assertNotEqual(images, [])

        for img in images:
            self.assertTrue(os.path.exists(img.path))
            self.assertNotEqual(img.s_label, '')
            self.assertNotEqual(img.credit, '')

            self.assertIn('Acid Weed', img.s_label)
            self.assertEqual(img.g_label, 'Acid Weed')

    def test_load_algae(self) -> None:
        algae_root = collection.make_root('Algae')
        images = collection.load_category(algae_root)
        self.assertNotEqual(images, [])

        for img in images:
            self.assertTrue(os.path.exists(img.path))
            self.assertNotEqual(img.credit, '', img)
            self.assertEqual(img.category, 'Algae')

    def test_load_fish(self) -> None:
        fish_root = collection.make_root('Fish')
        images = collection.load_category(fish_root)
        self.assertNotEqual(images, [])

        for img in images:
            self.assertTrue(os.path.exists(img.path))
            self.assertNotEqual(img.credit, '', img)
            self.assertEqual(img.category, 'Fish')

    def test_load_inverts(self) -> None:
        inverts_root = collection.make_root('Inverts')
        images = collection.load_category(inverts_root)
        self.assertNotEqual(images, [])

        for img in images:
            self.assertTrue(os.path.exists(img.path))
            self.assertNotEqual(img.credit, '', img)
            self.assertEqual(img.category, 'Inverts')

    def test_credits(self) -> None:
        images = collection.load_images()
        people = {img.credit for img in images}
        self.assertIn('Dan Abbott', people)

    def test_uniqueness(self) -> None:
        images = collection.load_images()
        ids = {img.id for img in images}
        self.assertEqual(len(ids), len(images))

    def test_ignored_categories(self) -> None:
        fish_root = collection.make_root('Fish')
        images = collection.load_category(fish_root)

        for img in images:
            self.assertNotEqual(img.g_label, 'YOY')

    def test_sub_category(self) -> None:
        greenling_root = collection.make_root('Fish/Kelp Greenling')
        images = collection.load_root(greenling_root)
        self.assertNotEqual(images, [])

        for img in images:
            self.assertTrue(os.path.exists(img.path))
            self.assertNotEqual(img.credit, '', img)

            self.assertIn('Kelp Greenling', img.g_label)
            *_, gender = img.g_label.split(' ')
            self.assertIn(gender, ['Male', 'Female', 'Juvenile'])

    def test_label_conversions(self) -> None:
        cases = [
            ('Algae/Pterygophora (Woody Kelp)', 'Woody Kelp'),
            ('Algae/Sargassum horneri (Horn Weed)', 'Horn Weed'),
            ('Algae/Laminaria setchelii (Torn Kelp)', 'Torn Kelp'),
            ('Algae/Sargassum muticum (Wire Weed)', 'Wire Weed'),
            ('Algae/Five-ribbed Kelp (Costaria costata)', 'Five ribbed Kelp'),
            ('Algae/Three-ribbed Kelp (Cymathaera triplicata)', 'Three ribbed Kelp'),
            ("Inverts/Stimpson's Sun Star", 'Blue Striped Sun Star'),
        ]

        for case in cases:
            original, expected = case
            root = collection.make_root(original)
            images = collection.load_root(root)
            self.assertNotEqual(images, [])

            self.assertEqual(images[0].g_label, expected)

    def test_hyphen_author(self) -> None:
        perch_root = collection.make_root('Fish/Shiner Perch')
        images = collection.load_root(perch_root)
        authors = {img.credit for img in images}
        self.assertIn('Shou-Wei Chang', authors)
