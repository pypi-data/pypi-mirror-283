# http://pyrocko.org - GPLv3
#
# The pyrockoeost Developers, 21st Century
# ---|P------/S----------~Lg----------

import re
import logging
import os.path as op

import numpy as num

from pyrockoeost import io, trace, util
from pyrockoeost.progress import progress
from pyrockoeost.has_paths import Path, HasPaths
from pyrockoeost.guts import Dict, String, Choice, Float, List, Timestamp, \
    StringChoice, IntChoice, Defer, load_all, clone
from pyrockoeost.squirrel.dataset import Dataset
from pyrockoeost.squirrel.client.local import LocalData
from pyrockoeost.squirrel.error import ToolError
from pyrockoeost.squirrel.model import CodesNSLCE
from pyrockoeost.squirrel.operators.base import NetworkGrouping, StationGrouping, \
    ChannelGrouping, SensorGrouping

tts = util.time_to_str

guts_prefix = 'jackseis'
logger = logging.getLogger('psq.cli.jackseis')


def make_task(*args):
    return progress.task(*args, logger=logger)


def parse_rename_rule_from_string(s):
    s = s.strip()
    if re.match(r'^([^:,]*:[^:,]*,?)+', s):
        return dict(
            x.split(':') for x in s.strip(',').split(','))
    else:
        return s


class JackseisError(ToolError):
    pass


class Chain(object):
    def __init__(self, node, parent=None):
        self.node = node
        self.parent = parent

    def mcall(self, name, *args, **kwargs):
        ret = []
        if self.parent is not None:
            ret.append(self.parent.mcall(name, *args, **kwargs))

        ret.append(getattr(self.node, name)(*args, **kwargs))
        return ret

    def fcall(self, name, *args, **kwargs):
        v = getattr(self.node, name)(*args, **kwargs)
        if v is None and self.parent is not None:
            return self.parent.fcall(name, *args, **kwargs)
        else:
            return v

    def get(self, name):
        v = getattr(self.node, name)
        if v is None and self.parent is not None:
            return self.parent.get(name)
        else:
            return v

    def dget(self, name, k):
        v = getattr(self.node, name).get(k, None)
        if v is None and self.parent is not None:
            return self.parent.dget(name, k)
        else:
            return v


class OutputFormatChoice(StringChoice):
    choices = io.allowed_formats('save')


class OutputDataTypeChoice(StringChoice):
    choices = ['int32', 'int64', 'float32', 'float64']
    name_to_dtype = {
        'int32': num.int32,
        'int64': num.int64,
        'float32': num.float32,
        'float64': num.float64}


class TraversalChoice(StringChoice):
    choices = ['network', 'station', 'channel', 'sensor']
    name_to_grouping = {
        'network': NetworkGrouping(),
        'station': StationGrouping(),
        'sensor': SensorGrouping(),
        'channel': ChannelGrouping()}


class Converter(HasPaths):

    in_dataset = Dataset.T(optional=True)
    in_path = String.T(optional=True)
    in_paths = List.T(String.T(optional=True))

    codes = List.T(CodesNSLCE.T(), optional=True)

    rename = Dict.T(
        String.T(),
        Choice.T([
            String.T(),
            Dict.T(String.T(), String.T())]))
    tmin = Timestamp.T(optional=True)
    tmax = Timestamp.T(optional=True)
    tinc = Float.T(optional=True)

    downsample = Float.T(optional=True)

    out_path = Path.T(optional=True)
    out_sds_path = Path.T(optional=True)
    out_format = OutputFormatChoice.T(optional=True)
    out_data_type = OutputDataTypeChoice.T(optional=True)
    out_mseed_record_length = IntChoice.T(
        optional=True,
        choices=list(io.mseed.VALID_RECORD_LENGTHS))
    out_mseed_steim = IntChoice.T(
        optional=True,
        choices=[1, 2])
    out_meta_path = Path.T(optional=True)

    traversal = TraversalChoice.T(optional=True)

    parts = List.T(Defer('Converter.T'))

    @classmethod
    def add_arguments(cls, p):
        p.add_squirrel_query_arguments(without=['time'])

        p.add_argument(
            '--tinc',
            dest='tinc',
            type=float,
            metavar='SECONDS',
            help='Set time length of output files [s].')

        p.add_argument(
            '--downsample',
            dest='downsample',
            type=float,
            metavar='RATE',
            help='Downsample to RATE [Hz].')

        p.add_argument(
            '--out-path',
            dest='out_path',
            metavar='TEMPLATE',
            help='Set output path to TEMPLATE. Available placeholders '
                 'are %%n: network, %%s: station, %%l: location, %%c: '
                 'channel, %%b: begin time, %%e: end time, %%j: julian day of '
                 'year. The following additional placeholders use the window '
                 'begin and end times rather than trace begin and end times '
                 '(to suppress producing many small files for gappy traces), '
                 '%%(wmin_year)s, %%(wmin_month)s, %%(wmin_day)s, %%(wmin)s, '
                 '%%(wmin_jday)s, %%(wmax_year)s, %%(wmax_month)s, '
                 '%%(wmax_day)s, %%(wmax)s, %%(wmax_jday)s. '
                 "Example: --out-path='data/%%s/trace-%%s-%%c.mseed'")

        p.add_argument(
            '--out-sds-path',
            dest='out_sds_path',
            metavar='PATH',
            help='Set output path to create SDS (https://www.seiscomp.de'
                 '/seiscomp3/doc/applications/slarchive/SDS.html), rooted at '
                 'the given path. Implies --tinc=86400. '
                 'Example: --out-sds-path=data/sds')

        p.add_argument(
            '--out-format',
            dest='out_format',
            choices=io.allowed_formats('save'),
            metavar='FORMAT',
            help='Set output file format. Choices: %s' % io.allowed_formats(
                'save', 'cli_help', 'mseed'))

        p.add_argument(
            '--out-data-type',
            dest='out_data_type',
            choices=OutputDataTypeChoice.choices,
            metavar='DTYPE',
            help='Set numerical data type. Choices: %s. The output file '
                 'format must support the given type. By default, the data '
                 'type is kept unchanged.' % ', '.join(
                    OutputDataTypeChoice.choices))

        p.add_argument(
            '--out-mseed-record-length',
            dest='out_mseed_record_length',
            type=int,
            choices=io.mseed.VALID_RECORD_LENGTHS,
            metavar='INT',
            help='Set the mseed record length in bytes. Choices: %s. '
                 'Default is 4096 bytes, which is commonly used for archiving.'
                 % ', '.join(str(b) for b in io.mseed.VALID_RECORD_LENGTHS))

        p.add_argument(
            '--out-mseed-steim',
            dest='out_mseed_steim',
            type=int,
            choices=(1, 2),
            metavar='INT',
            help='Set the mseed STEIM compression. Choices: 1 or 2. '
                 'Default is STEIM-2, which can compress full range int32. '
                 'Note: STEIM-2 is limited to 30 bit dynamic range.')

        p.add_argument(
            '--out-meta-path',
            dest='out_meta_path',
            metavar='PATH',
            help='Set output path for station metadata (StationXML) export.')

        p.add_argument(
            '--traversal',
            dest='traversal',
            metavar='GROUPING',
            choices=TraversalChoice.choices,
            help='By default the outermost processing loop is over time. '
                 'Add outer loop with given GROUPING. Choices: %s'
                 % ', '.join(TraversalChoice.choices))

        p.add_argument(
            '--rename-network',
            dest='rename_network',
            metavar='REPLACEMENT',
            help="""
Replace network code. REPLACEMENT can be a string for direct replacement, a
mapping for selective replacement, or a regular expression for tricky
replacements. Examples: Direct replacement: ```XX``` - set all network codes to
```XX```. Mapping: ```AA:XX,BB:YY``` - replace ```AA``` with ```XX``` and
```BB``` with ```YY```. Regular expression: ```/A(\\d)/X\\1/``` - replace
```A1``` with ```X1``` and ```A2``` with ```X2``` etc.
""".strip())

        p.add_argument(
            '--rename-station',
            dest='rename_station',
            metavar='REPLACEMENT',
            help='Replace station code. See ``--rename-network``.')

        p.add_argument(
            '--rename-location',
            dest='rename_location',
            metavar='REPLACEMENT',
            help='Replace location code. See ``--rename-network``.')

        p.add_argument(
            '--rename-channel',
            dest='rename_channel',
            metavar='REPLACEMENT',
            help='Replace channel code. See ``--rename-network``.')

        p.add_argument(
            '--rename-extra',
            dest='rename_extra',
            metavar='REPLACEMENT',
            help='Replace extra code. See ``--rename-network``. Note: the '
                 '```extra``` code is not available in Mini-SEED.')

    @classmethod
    def from_arguments(cls, args):
        kwargs = args.squirrel_query

        rename = {}
        for (k, v) in [
                ('network', args.rename_network),
                ('station', args.rename_station),
                ('location', args.rename_location),
                ('channel', args.rename_channel),
                ('extra', args.rename_extra)]:

            if v is not None:
                rename[k] = parse_rename_rule_from_string(v)

        obj = cls(
            downsample=args.downsample,
            out_format=args.out_format,
            out_path=args.out_path,
            tinc=args.tinc,
            out_sds_path=args.out_sds_path,
            out_data_type=args.out_data_type,
            out_mseed_record_length=args.out_mseed_record_length,
            out_mseed_steim=args.out_mseed_steim,
            out_meta_path=args.out_meta_path,
            traversal=args.traversal,
            rename=rename,
            **kwargs)

        obj.validate()
        return obj

    def add_dataset(self, sq):
        if self.in_dataset is not None:
            sq.add_dataset(self.in_dataset)

        if self.in_path is not None:
            ds = Dataset(sources=[LocalData(paths=[self.in_path])])
            ds.set_basepath_from(self)
            sq.add_dataset(ds)

        if self.in_paths:
            ds = Dataset(sources=[LocalData(paths=self.in_paths)])
            ds.set_basepath_from(self)
            sq.add_dataset(ds)

    def get_effective_rename_rules(self, chain):
        d = {}
        for k in ['network', 'station', 'location', 'channel']:
            v = chain.dget('rename', k)
            if isinstance(v, str):
                m = re.match(r'/([^/]+)/([^/]*)/', v)
                if m:
                    try:
                        v = (re.compile(m.group(1)), m.group(2))
                    except Exception:
                        raise JackseisError(
                            'Invalid replacement pattern: /%s/' % m.group(1))

            d[k] = v

        return d

    def get_effective_out_path(self):
        nset = sum(x is not None for x in (
            self.out_path,
            self.out_sds_path))

        if nset > 1:
            raise JackseisError(
                'More than one out of [out_path, out_sds_path] set.')

        is_sds = False
        if self.out_path:
            out_path = self.out_path

        elif self.out_sds_path:
            out_path = op.join(
                self.out_sds_path,
                '%(wmin_year)s/%(network)s/%(station)s/%(channel)s.D'
                '/%(network)s.%(station)s.%(location)s.%(channel)s.D'
                '.%(wmin_year)s.%(wmin_jday)s')
            is_sds = True
        else:
            out_path = None

        if out_path is not None:
            return self.expand_path(out_path), is_sds
        else:
            return None

    def get_effective_out_meta_path(self):
        if self.out_meta_path is not None:
            return self.expand_path(self.out_meta_path)
        else:
            return None

    def do_rename(self, rules, tr):
        rename = {}
        for k in ['network', 'station', 'location', 'channel']:
            v = rules.get(k, None)
            if isinstance(v, str):
                rename[k] = v
            elif isinstance(v, dict):
                try:
                    oldval = getattr(tr, k)
                    rename[k] = v[oldval]
                except KeyError:
                    raise ToolError(
                        'No mapping defined for %s code "%s".' % (k, oldval))

            elif isinstance(v, tuple):
                pat, repl = v
                oldval = getattr(tr, k)
                newval, n = pat.subn(repl, oldval)
                if n:
                    rename[k] = newval

        tr.set_codes(**rename)

    def convert(self, args, chain=None):
        if chain is None:
            defaults = clone(g_defaults)
            defaults.set_basepath_from(self)
            chain = Chain(defaults)

        chain = Chain(self, chain)

        if self.parts:
            task = make_task('Jackseis parts')
            for part in task(self.parts):
                part.convert(args, chain)

            del task

        else:
            sq = args.make_squirrel()

            cli_overrides = Converter.from_arguments(args)
            cli_overrides.set_basepath('.')

            chain = Chain(cli_overrides, chain)

            chain.mcall('add_dataset', sq)

            tmin = chain.get('tmin')
            tmax = chain.get('tmax')
            tinc = chain.get('tinc')
            codes = chain.get('codes')
            downsample = chain.get('downsample')
            out_path, is_sds = chain.fcall('get_effective_out_path') \
                or (None, False)

            if is_sds and tinc != 86400.:
                logger.warning('Setting time window to 1 day to generate SDS.')
                tinc = 86400.0

            out_format = chain.get('out_format')
            out_data_type = chain.get('out_data_type')

            out_meta_path = chain.fcall('get_effective_out_meta_path')

            if out_meta_path is not None:
                sx = sq.get_stationxml(codes=codes, tmin=tmin, tmax=tmax)
                util.ensuredirs(out_meta_path)
                sx.dump_xml(filename=out_meta_path)
                if out_path is None:
                    return

            target_deltat = None
            if downsample is not None:
                target_deltat = 1.0 / float(downsample)

            save_kwargs = {}
            if out_format == 'mseed':
                save_kwargs['record_length'] = chain.get(
                    'out_mseed_record_length')
                save_kwargs['steim'] = chain.get(
                    'out_mseed_steim')

            traversal = chain.get('traversal')
            if traversal is not None:
                grouping = TraversalChoice.name_to_grouping[traversal]
            else:
                grouping = None

            tpad = 0.0
            if target_deltat is not None:
                tpad += target_deltat * 50.

            task = None
            rename_rules = self.get_effective_rename_rules(chain)
            for batch in sq.chopper_waveforms(
                    tmin=tmin, tmax=tmax, tpad=tpad, tinc=tinc,
                    codes=codes,
                    snap_window=True,
                    grouping=grouping):

                if task is None:
                    task = make_task(
                        'Jackseis blocks', batch.n * batch.ngroups)

                tlabel = '%s%s - %s' % (
                    'groups %i / %i: ' % (batch.igroup, batch.ngroups)
                    if batch.ngroups > 1 else '',
                    util.time_to_str(batch.tmin),
                    util.time_to_str(batch.tmax))

                task.update(batch.i + batch.igroup * batch.n, tlabel)

                twmin = batch.tmin
                twmax = batch.tmax

                traces = batch.traces

                if target_deltat is not None:
                    out_traces = []
                    for tr in traces:
                        try:
                            tr.downsample_to(
                                target_deltat, snap=True, demean=False,
                                allow_upsample_max=4)

                            out_traces.append(tr)

                        except (trace.TraceTooShort, trace.NoData):
                            pass

                    traces = out_traces

                for tr in traces:
                    self.do_rename(rename_rules, tr)

                if out_data_type:
                    for tr in traces:
                        tr.ydata = tr.ydata.astype(
                            OutputDataTypeChoice.name_to_dtype[out_data_type])

                chopped_traces = []
                for tr in traces:
                    try:
                        otr = tr.chop(twmin, twmax, inplace=False)
                        chopped_traces.append(otr)
                    except trace.NoData:
                        pass

                traces = chopped_traces

                if out_path is not None:
                    try:
                        io.save(
                            traces, out_path,
                            format=out_format,
                            overwrite=args.force,
                            additional=dict(
                                wmin_year=tts(twmin, format='%Y'),
                                wmin_month=tts(twmin, format='%m'),
                                wmin_day=tts(twmin, format='%d'),
                                wmin_jday=tts(twmin, format='%j'),
                                wmin=tts(twmin, format='%Y-%m-%d_%H-%M-%S'),
                                wmax_year=tts(twmax, format='%Y'),
                                wmax_month=tts(twmax, format='%m'),
                                wmax_day=tts(twmax, format='%d'),
                                wmax_jday=tts(twmax, format='%j'),
                                wmax=tts(twmax, format='%Y-%m-%d_%H-%M-%S')),
                            **save_kwargs)

                    except io.FileSaveError as e:
                        raise JackseisError(str(e))

                else:
                    for tr in traces:
                        print(tr.summary)

            if task:
                task.done()


g_defaults = Converter(
    out_mseed_record_length=4096,
    out_format='mseed',
    out_mseed_steim=2)


headline = 'Convert waveform archive data.'


def make_subparser(subparsers):
    return subparsers.add_parser(
        'jackseis',
        help=headline,
        description=headline)


def setup(parser):
    parser.add_squirrel_selection_arguments()

    parser.add_argument(
        '--config',
        dest='config_path',
        metavar='NAME',
        help='File containing `jackseis.Converter` settings.')

    parser.add_argument(
        '--force',
        dest='force',
        action='store_true',
        default=False,
        help='Force overwriting of existing files.')

    Converter.add_arguments(parser)


def run(parser, args):
    if args.config_path:
        try:
            converters = load_all(filename=args.config_path)
        except Exception as e:
            raise ToolError(str(e))

        for converter in converters:
            if not isinstance(converter, Converter):
                raise ToolError(
                    'Config file should only contain '
                    '`jackseis.Converter` objects.')

            converter.set_basepath(op.dirname(args.config_path))

    else:
        converter = Converter()
        converter.set_basepath('.')
        converters = [converter]

    with progress.view():
        task = make_task('Jackseis jobs')
        for converter in task(converters):
            converter.convert(args)
