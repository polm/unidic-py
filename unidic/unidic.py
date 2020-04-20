import os
import sys
from wasabi import msg

def get_version(dicdir):
    try:
        vpath = os.path.join(dicdir, 'version')
        with open(vpath) as vfile:
            return vfile.read().strip()
    except FileNotFoundError:
        return '0'

_curdir = os.path.dirname(__file__)

# This will be used elsewhere to initialize the tagger
DICDIR = os.path.join(_curdir, 'dicdir')
VERSION = get_version(DICDIR)

