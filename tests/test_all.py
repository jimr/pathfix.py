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

        fixed = pathfix.fix_path('Y:\some path\with%20spaces', self.cfg)
        self.assertEqual(
            fixed,
            '/media/network/host2/share2/some path/with spaces'
        )

    def test_drive_maps_with_file_prefix(self):
        fixed = pathfix.fix_path(r'file:///X:/some/path', self.cfg)
        self.assertEqual(fixed, '/media/network/host1/share1/some/path')

    def test_file_prefix(self):
        fixed = pathfix.fix_path(r'file://host1/share1/some/path', self.cfg)
        self.assertEqual(fixed, '/media/network/host1/share1/some/path')

    def test_smb_prefix(self):
        fixed = pathfix.fix_path(r'smb://host2/share2/some/path', self.cfg)
        self.assertEqual(fixed, '/media/network/host2/share2/some/path')


if __name__ == '__main__':
    unittest.main()
