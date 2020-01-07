import os
import sys

def get_version(dicdir):
    with open(dicdir + '/version') as vfile:
        return vfile.read().strip()

_curdir = os.path.dirname(__file__)

# This will be used elsewhere to initialize the tagger
DICDIR = os.path.join(_curdir, 'dicdir')
VERSION = get_version(DICDIR)

if VERSION == '0':
    print("No data installed, downloading 2.1.2.", file=sys.stderr)
    from .download import download
    download('2.1.2')

    DICDIR = os.path.join(_curdir, 'dicdir')
    VERSION = get_version(DICDIR)

