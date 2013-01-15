#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# See https://github.com/jimr/pathfix.py/blob/master/README.rst for usage

import os
import re

try:
    from ConfigParser import SafeConfigParser as ConfigParser
except ImportError:  # py3k
    import sys
    minor = sys.version_info[1]
    if minor >= 2:
        # SafeConfigParser is deprecated as of 3.2
        from configparser import ConfigParser
    else:
        from configparser import SafeConfigParser as ConfigParser

FILE_PREFIXES = ['file:///', 'file://', 'smb://']
DRIVE_RE = re.compile(r'^[A-Z]:(\\|/)')


def fix_path(path, cfg=None):
    """Fix the given path.

    If ``cfg`` is provided, we read the configuration from that path instead
    of the default.

    """
    if not cfg:
        # If we're running from a .pyc file, there won't be a symlink, so
        # finding our way back to the config.ini won't work unless we do it
        # from the symlinked .py file.
        fname = __file__
        if fname.endswith('.pyc'):
            fname = fname[:-1]

        cfg = os.path.join(
            # Allow symlinking pathfix.py to, eg, /usr/local/bin
            os.path.dirname(os.path.realpath(fname)),
            'config.ini',
        )

    parser = ConfigParser()
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

    if DRIVE_RE.match(path):
        drive = path[0].upper()
        if drive not in drive_map:
            raise Exception("Unknown drive mapping: %s" % drive)
        path = DRIVE_RE.split(path)[-1]
        prefix += '/%s/%s/' % drive_map.get(drive)

    path = path.replace('\\', '/').replace('%20', ' ')

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
