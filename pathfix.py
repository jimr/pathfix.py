#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# See https://github.com/jimr/pathfix.py/blob/master/README.rst for usage

import os
import re
import sys

from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read(os.path.join(
    # Allow symlinking pathfix.py to, eg, /usr/local/bin
    os.path.dirname(os.path.realpath(__file__)),
    'config.ini',
))

FILE_PREFIXES = ['file:///', 'smb://']
DRIVE_RE = re.compile(r'^[A-Z]:\\')
DRIVE_MAP = dict()

for option in parser.options('drive_maps'):
    DRIVE_MAP[option.upper()] = tuple(
        parser.get('drive_maps', option).split(':')
    )


def main():
    path = sys.argv[1]

    for prefix in FILE_PREFIXES:
        if path[:len(prefix)] == prefix:
            path = path[len(prefix):]

    prefix = parser.get('main', 'network_root')

    if DRIVE_RE.search(path):
        if path[0] not in DRIVE_MAP:
            raise Exception("Unknown drive mapping: %s" % path[0])
        network_path = DRIVE_MAP.get(path[0])
        path = path[3:]
        prefix += '/%s/%s/' % network_path

    path = path.replace('\\', '/')
    path = path.replace('%20', ' ')

    print '%s%s' % (prefix, path)

if __name__ == '__main__':
    main()
