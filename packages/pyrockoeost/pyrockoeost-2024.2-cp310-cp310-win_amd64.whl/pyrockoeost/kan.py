
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: pyrockoeost.kan\n')
    sys.stderr.write('           -> should now use: pyrockoeost.io.kan\n\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: pyrockoeost.kan\n')
    sys.stderr.write('              -> should now use: pyrockoeost.io.kan\n\n')
    raise ImportError('pyrockoeost module "pyrockoeost.kan" has been renamed to "pyrockoeost.io.kan".')

from pyrockoeost.io.kan import *
