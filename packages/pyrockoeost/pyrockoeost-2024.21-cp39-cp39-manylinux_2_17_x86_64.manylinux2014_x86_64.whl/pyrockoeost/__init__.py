# https://pyrocko.org - GPLv3
#
# The pyrockoeost Developers, 21st Century
# ---|P------/S----------~Lg----------

try:
    from .info import *  # noqa
    __version__ = version  # noqa
except ImportError:
    pass  # not available in dev mode

grumpy = 0  # noqa


def get_logger():
    from .util import logging
    return logging.getLogger('pyrockoeost')


class ExternalProgramMissing(Exception):
    pass


def make_squirrel(*args, **kwargs):
    from pyrockoeost.squirrel import Squirrel
    return Squirrel(*args, **kwargs)


def snuffle(*args, **kwargs):
    '''
    Start Snuffler.

    Calls :py:func:`pyrockoeost.gui.snuffler.snuffle`
    '''

    from pyrockoeost import deps

    deps.require('PyQt5.Qt')
    deps.require('PyQt5.QtWebEngine')

    from pyrockoeost.gui.snuffler import snuffler
    return snuffler.snuffle(*args, **kwargs)


def sparrow(*args, **kwargs):
    '''
    Start Sparrow.

    Calls :py:func:`pyrockoeost.gui.sparrow.main`.
    '''

    from pyrockoeost import deps

    deps.require('vtk')
    deps.require('PyQt5.Qt')
    # deps.import_optional('kite', 'InSAR visualization')

    from pyrockoeost.gui.sparrow.main import main
    return main(*args, **kwargs)


def drum(*args, **kwargs):
    '''
    Start Drum Plot.

    Calls :py:func:`pyrockoeost.gui.drum.main`.
    '''

    from pyrockoeost import deps

    deps.require('PyQt5.Qt')
    deps.require('serial')

    from pyrockoeost.gui.drum.main import main
    return main(*args, **kwargs)
