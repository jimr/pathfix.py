#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# See https://github.com/jimr/pathfix.py/blob/master/README.rst for usage

import os
import re

try:
    from urllib import unquote
except ImportError:  # py3k
    from urllib.parse import unquote

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


__all__ = ['fix_path']


class ConfigurationError(Exception):
    pass


FILE_PREFIXES = ['file:///', 'file://', 'smb://']
DRIVE_RE = re.compile(r'^[A-Z](:|\|)(\\|/)')


def _get_config(fname=None):
    if not fname:
        fnames = []
        # If we're running from a .pyc file, there won't be a symlink, so
        # finding our way back to the config.ini won't work unless we do it
        # from the symlinked .py file.
        this_file = __file__
        if this_file.endswith('.pyc'):
            this_file = this_file[:-1]

        fname = os.path.join(
            # Allow symlinking pathfix.py to, eg, /usr/local/bin
            os.path.dirname(os.path.realpath(this_file)),
            'config.ini',
        )
        fnames.append(fname)

        # Check for $HOME/.config/pathfix/config.ini
        if not os.path.exists(fname):
            fname = os.path.join(
                os.getenv('HOME'), '.config', 'pathfix', 'config.ini'
            )
            fnames.append(fname)

        if not os.path.exists(fname):
            raise ConfigurationError(
                "Unable to find configuration file. Tried:\n * %s" %
                '\n * '.join(fnames)
            )

    config = ConfigParser()
    config.read(fname)

    return config


def fix_path(path, cfg=None):
    """Fix the given path.

    If ``cfg`` is provided, we read the configuration from that path instead
    of the default.

    """
    config = _get_config(cfg)

    drive_map = dict()
    for option in config.options('drive_maps'):
        drive_map[option.upper()] = tuple(
            config.get('drive_maps', option).split(':')
        )

    for prefix in FILE_PREFIXES:
        if path.startswith(prefix):
            path = path[len(prefix):]
            break

    prefix = config.get('main', 'network_root')

    if DRIVE_RE.match(path):
        drive = path[0].upper()
        if drive not in drive_map:
            raise ConfigurationError("Unknown drive mapping: %s" % drive)
        path = DRIVE_RE.split(path)[-1]
        prefix += '/%s/%s/' % drive_map.get(drive)

    path = unquote(path.replace('\\', '/'))

    if not (path.startswith('/') or prefix.endswith('/')):
        path = '/%s' % path

    return os.path.normpath('%s%s' % (prefix, path))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='the path to fix')
    parser.add_argument('--config', dest='config', help='config file path')
    args = parser.parse_args()

    print(fix_path(args.path, args.config))


if __name__ == '__main__':
    main()
