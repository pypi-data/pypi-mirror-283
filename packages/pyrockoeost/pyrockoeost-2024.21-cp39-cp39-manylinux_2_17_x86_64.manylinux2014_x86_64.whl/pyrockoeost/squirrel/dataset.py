# http://pyrocko.org - GPLv3
#
# The pyrockoeost Developers, 21st Century
# ---|P------/S----------~Lg----------

import os.path as op
import logging

from pyrockoeost.guts import List, load, StringPattern

from ..has_paths import HasPaths
from .client.base import Source
from .error import SquirrelError
from .selection import re_persistent_name
from .operators.base import Operator

guts_prefix = 'squirrel'

logger = logging.getLogger('psq.dataset')


class PersistentID(StringPattern):
    pattern = re_persistent_name


class Dataset(HasPaths):
    '''
    Dataset description.
    '''
    sources = List.T(Source.T())
    operators = List.T(Operator.T())

    def setup(self, squirrel, check=True):
        for source in self.sources:
            squirrel.add_source(
                source, check=check)

        for operator in self.operators:
            squirrel.add_operator(operator)

        squirrel.update_operator_mappings()


def read_dataset(path):
    '''
    Read dataset description file.
    '''
    try:
        dataset = load(filename=path)
    except OSError:
        raise SquirrelError(
            'Cannot read dataset file: %s' % path)

    if not isinstance(dataset, Dataset):
        raise SquirrelError('Invalid dataset file "%s".' % path)

    dataset.set_basepath(op.dirname(path) or '.')
    return dataset


__all__ = [
    'PersistentID',
    'Dataset',
    'read_dataset',
]
