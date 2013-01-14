#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# See https://github.com/jimr/pathfix.py/blob/master/README.rst for usage

import os
import re

try:
    from ConfigParser import SafeConfigParser
except:  # py3k
    from configparser import SafeConfigParser

FILE_PREFIXES = ['file:///', 'file://', 'smb://']
DRIVE_RE = re.compile(r'^[A-Z]:(\\?|//?)')


def fix_path(path, cfg=None):
    if not cfg:
        cfg = os.path.join(
            # Allow symlinking pathfix.py to, eg, /usr/local/bin
            os.path.dirname(os.path.realpath(__file__)),
            'config.ini',
        )

    parser = SafeConfigParser()
    parser.read(cfg)

    drive_map = dict()
    for option in parser.options('drive_maps'):
        drive_map[option.upper()] = tuple(
            parser.get('drive_maps', option).split(':')
        )

    for prefix in FILE_PREFIXES:
        if path.startswith(prefix):
            path = path[len(prefix):]
            break

    prefix = parser.get('main', 'network_root')

    if DRIVE_RE.search(path):
        if path[0] not in drive_map:
            raise Exception("Unknown drive mapping: %s" % path[0])
        network_path = drive_map.get(path[0])
        path = path[3:]
        prefix += '/%s/%s/' % network_path

    path = path.replace('\\', '/')
    path = path.replace('%20', ' ')

    if not (path.startswith('/') or prefix.endswith('/')):
        path = '/%s' % path

    return '%s%s' % (prefix, path)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='the path to fix')
    parser.add_argument('--config', dest='config', help='config file path')
    args = parser.parse_args()

    print(fix_path(args.path, args.config))


if __name__ == '__main__':
    main()
