#!/usr/bin/python3

import os
import unittest

import image


class TestLoad(unittest.TestCase):
    def test_load_bull_kelp(self) -> None:
        bull_kelp_root = image.make_root('Algae/Bull Kelp')
        images = image.load_root(bull_kelp_root)
        self.assertNotEqual(images, [])

        for img in images:
            self.assertTrue(os.path.exists(img.path))
            self.assertNotEqual(img.s_label, '')
            self.assertNotEqual(img.credit, '')

            self.assertIn('Bull Kelp', img.s_label)
            self.assertEqual(img.g_label, 'Bull Kelp')

    def test_load_acid_weed(self) -> None:
        acid_weed_root = image.make_root('Algae/Acid Weed (Desmarestia ligulata)')
        images = image.load_root(acid_weed_root)
        self.assertNotEqual(images, [])

        for img in images:
            self.assertTrue(os.path.exists(img.path))
            self.assertNotEqual(img.s_label, '')
            self.assertNotEqual(img.credit, '')

            self.assertIn('Acid Weed', img.s_label)
            self.assertEqual(img.g_label, 'Acid Weed')

    def test_load_algae(self) -> None:
        algae_root = image.make_root('Algae')
        images = image.load_category(algae_root)
        self.assertNotEqual(images, [])

        for img in images:
            self.assertTrue(os.path.exists(img.path))
            self.assertNotEqual(img.credit, '', img)

    def test_load_fish(self) -> None:
        fish_root = image.make_root('Fish')
        images = image.load_category(fish_root)
        self.assertNotEqual(images, [])

        for img in images:
            self.assertTrue(os.path.exists(img.path))
            self.assertNotEqual(img.credit, '', img)

    def test_load_inverts(self) -> None:
        inverts_root = image.make_root('Inverts')
        images = image.load_category(inverts_root)
        self.assertNotEqual(images, [])

        for img in images:
            self.assertTrue(os.path.exists(img.path))
            self.assertNotEqual(img.credit, '', img)

    def test_credits(self) -> None:
        images = image.load_everything()
        people = {img.credit for img in images}
        self.assertIn('Dan Abbott', people)

    def test_uniqueness(self) -> None:
        images = image.load_everything()
        ids = {img.id for img in images}
        self.assertEqual(len(ids), len(images))


if __name__ == '__main__':
    unittest.main()
