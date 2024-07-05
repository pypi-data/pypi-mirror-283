# http://pyrocko.org - GPLv3
#
# The pyrockoeost Developers, 21st Century
# ---|P------/S----------~Lg----------

from pyrockoeost.io.io_common import get_stats, touch  # noqa
from ... import model

SEGMENT_SIZE = 1024*1024


def provided_formats():
    return ['mseed']


def detect(first512):
    from pyrockoeost.io import mseed

    if mseed.detect(first512):
        return 'mseed'
    else:
        return None


def iload(format, file_path, segment, content):
    assert format == 'mseed'
    from pyrockoeost.io import mseed

    load_data = 'waveform' in content

    if segment is None:
        offset = 0
        nsegments = 0
    else:
        offset = segment
        nsegments = 1

    file_segment = None
    itr = 0
    for tr in mseed.iload(
            file_path, load_data=load_data,
            offset=offset, segment_size=SEGMENT_SIZE, nsegments=nsegments):

        if file_segment != tr.meta['offset_start']:
            itr = 0
            file_segment = tr.meta['offset_start']

        nsamples = int(round((tr.tmax - tr.tmin) / tr.deltat)) + 1
        nut = model.make_waveform_nut(
            file_segment=file_segment,
            file_element=itr,
            codes=tr.codes,
            tmin=tr.tmin,
            tmax=tr.tmin + tr.deltat * nsamples,
            deltat=tr.deltat)

        if 'waveform' in content:
            nut.content = tr

        yield nut
        itr += 1
