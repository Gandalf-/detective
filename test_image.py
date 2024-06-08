#!/usr/bin/python3

import os
import unittest

import image


class TestImage(unittest.TestCase):
    def test_image_root(self):
        exists = os.path.exists(image.image_root)
        assert exists

    def test_parse_name(self):
        filename = 'BullKelp_DavidHorwich.jpg'
        self.assertEqual(image.parse_name(filename), ('Bull Kelp', 'David Horwich'))

    def test_titlecase_to_spaces(self):
        self.assertEqual(image.titlecase_to_spaces('BullKelp'), 'Bull Kelp')
        self.assertEqual(image.titlecase_to_spaces('DavidHorwich'), 'David Horwich')


if __name__ == '__main__':
    unittest.main()
