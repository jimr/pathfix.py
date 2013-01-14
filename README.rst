==========
pathfix.py
==========

Using Linux? Tired of receiving emails with links to files of the form ``X:\some%20path\on\remote%20share\spreadsheet.xls``? Then we can help!

``pathfix.py`` takes an unusable path as input and prints a useful one as output. That's it.

It can handle Windows drive prefixes (if configured), and will also sort out ``file://`` and ``smb://`` prefixes.

Installation
============

Create a ``config.ini`` file that contains the root of your network mounts and any drive mappings (see ``config.example.ini`` to get started).

We assume all your network shares are mounted under a common root, with the form::

    /<network mount root>/<host name>/<share name>

To make sure it'll work with your environment, run the tests::

    python setup.py test

If installing from source, you may find it helpful to symlink ``pathfix.py`` to ``/usr/local/bin`` or somewhere else on your ``PATH``, or you can just ``python setup.py install`` and you'll get the ``pathfix`` executable on your path.

Alternatively, you can just ``pip install pathfix.py``.

If you install with ``pip``, you should probably make a ``config.ini`` somewhere in your home directory and set up an alias, e.g.::

    alias pathfix="pathfix --config $HOME/.config/pathfix.ini"

Usage
=====

For example, if you have this in your ``config.ini``::

    [main]
    network_root = /media/network

    [drive_maps]
    x = host1:share1
    y = host2:share2

Then you can do, for example::

    % pathfix "X:\some%20path\on\remote%20share\spreadsheet.xls"
    /media/network/host1/share1/some path/on/remote share/spreadsheet.xls

Which you can use in subshells to fix arguments to other applications, for example::

    % libreoffice "$(pathfix "X:\some%20path\on\remote%20share\spreadsheet.xls")"

