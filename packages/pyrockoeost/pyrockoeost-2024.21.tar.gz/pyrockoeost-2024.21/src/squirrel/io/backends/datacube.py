# http://pyrocko.org - GPLv3
#
# The pyrockoeost Developers, 21st Century
# ---|P------/S----------~Lg----------

from pyrockoeost.io.io_common import get_stats, touch  # noqa
from ... import model


def provided_formats():
    return ['datacube']


def detect(first512):
    from pyrockoeost.io import datacube

    if datacube.detect(first512):
        return 'datacube'
    else:
        return None


def iload(format, file_path, segment, content):
    assert format == 'datacube'

    from pyrockoeost.io import datacube

    load_data = 'waveform' in content

    for itr, tr in enumerate(datacube.iload(file_path, load_data=load_data)):

        nsamples = int(round((tr.tmax - tr.tmin) / tr.deltat)) + 1

        nut = model.make_waveform_nut(
            file_segment=0,
            file_element=itr,
            codes=tr.codes,
            tmin=tr.tmin,
            tmax=tr.tmin + tr.deltat * nsamples,
            deltat=tr.deltat)

        if 'waveform' in content:
            nut.content = tr

        yield nut
