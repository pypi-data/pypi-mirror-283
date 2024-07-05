# http://pyrocko.org - GPLv3
#
# The pyrockoeost Developers, 21st Century
# ---|P------/S----------~Lg----------


headline = 'Experimental Squirrel-powered Snuffler.'


def make_subparser(subparsers):
    return subparsers.add_parser(
        'snuffler',
        help=headline,
        description=headline)


def setup(parser):
    parser.add_squirrel_selection_arguments()


def run(parser, args):
    squirrel = args.make_squirrel()
    squirrel.pile.snuffle()
