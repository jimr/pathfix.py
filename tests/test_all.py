#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import pathfix


class TestAll(unittest.TestCase):
    def setUp(self):
        self.cfg = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'config.ini',
        )

    def test_drive_maps(self):
        fixed = pathfix.fix_path(r'X:\some\path', self.cfg)
        self.assertEqual(fixed, '/media/network/host1/share1/some/path')

        fixed = pathfix.fix_path(r'Y:\some path\with%20spaces', self.cfg)
        self.assertEqual(
            fixed,
            '/media/network/host2/share2/some path/with spaces'
        )

    def test_drive_maps_with_file_prefix(self):
        fixed = pathfix.fix_path('file://X|/some/path', self.cfg)
        self.assertEqual(fixed, '/media/network/host1/share1/some/path')

        fixed = pathfix.fix_path('file:///Y:/some path/with%20spaces', self.cfg)
        self.assertEqual(
            fixed,
            '/media/network/host2/share2/some path/with spaces'
        )

    def test_file_prefix(self):
        fixed = pathfix.fix_path('file://host1/share1/some/path', self.cfg)
        self.assertEqual(fixed, '/media/network/host1/share1/some/path')

    def test_smb_prefix(self):
        fixed = pathfix.fix_path('smb://host2/share2/some/path', self.cfg)
        self.assertEqual(fixed, '/media/network/host2/share2/some/path')

    def test_slash_prefix(self):
        fixed = pathfix.fix_path('//host1/share1/some/path', self.cfg)
        self.assertEqual(fixed, '/media/network/host1/share1/some/path')

        fixed = pathfix.fix_path(r'\\host2\share2\some\path', self.cfg)
        self.assertEqual(fixed, '/media/network/host2/share2/some/path')

    def test_unicode_path(self):
        fixed = pathfix.fix_path('file://host1/share1/ßøŋ', self.cfg)
        self.assertEqual(fixed, '/media/network/host1/share1/ßøŋ')

    def test_quoted_chars(self):
        fixed = pathfix.fix_path(r'X:\\is%23this%3Aa%20file%3F.txt', self.cfg)
        self.assertEqual(
            fixed,
            '/media/network/host1/share1/is#this:a file?.txt'
        )


if __name__ == '__main__':
    unittest.main()
