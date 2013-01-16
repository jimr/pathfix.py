==========
pathfix.py
==========

.. image:: https://travis-ci.org/jimr/pathfix.py.png
    :target: http://travis-ci.org/jimr/pathfix.py

Using Linux? Tired of receiving emails with links to files of the form ``X:\some%20path\on\remote%20share\spreadsheet.xls``? Then we can help!

``pathfix.py`` takes an unusable path as input and prints a useful one as output. That's it.

It can handle Windows drive prefixes (if configured), and will also sort out ``file://`` and ``smb://`` prefixes.

Should work with Python 2.4 - 3.3 and pypy (probably more, but that's as far as it's been tested).

Installation
============

Install system-wide with ``sudo pip install pathfix.py`` or ``sudo easy_install pathfix.py``.
This will put an executable named ``pathfix.py`` into your ``$PATH``.

Configuration
=============

You need to create a ``config.ini`` file that contains the root of your network mounts and any drive mappings (see config.example.ini_ or the example below to get started).

.. _config.example.ini: https://github.com/jimr/pathfix.py/blob/master/config.example.ini

By default, ``pathfix.py`` will check for ``$HOME/.config/pathfix/config.ini``, so it's best to keep your config there.
If you are installing from source, you can also just keep a ``config.ini`` in the source tree next to ``pathfix.py``.

We assume all your network shares are mounted under a common root, with the form::

    /<network mount root>/<host name>/<share name>

If you installed from source, you may find it helpful to symlink ``pathfix.py`` to ``/usr/local/bin`` or somewhere else on your ``PATH``, or you can just ``python setup.py install`` and you'll get the ``pathfix.py`` executable on your path.

Usage
=====

For example, if you have this in your ``config.ini``::

    [main]
    network_root = /media/network

    [drive_maps]
    x = host1:share1
    y = host2:share2

Then you can do, for example::

    % pathfix.py "X:\some%20path\on\remote%20share\spreadsheet.xls"
    /media/network/host1/share1/some path/on/remote share/spreadsheet.xls

Which you can use in subshells to fix arguments to other applications, for example::

    % libreoffice "$(pathfix.py "X:\some%20path\on\remote%20share\spreadsheet.xls")"

Development
===========

Pull requests are welcome, but please do include test cases that cover any updates.

There are no requirements unless you're using Python 2.4-2.6, or 3.0-3.1, in which case (if you're installing from source) you need to install ``argparse``::

    pip install -r requirements.txt

To make sure it all still works, run the tests::

    python setup.py test

