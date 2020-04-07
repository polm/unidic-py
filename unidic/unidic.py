import os
import sys
from wasabi import msg

def get_version(dicdir):
    with open(dicdir + '/version') as vfile:
        return vfile.read().strip()

_curdir = os.path.dirname(__file__)

# This will be used elsewhere to initialize the tagger
DICDIR = os.path.join(_curdir, 'dicdir')
VERSION = get_version(DICDIR)

if VERSION == '0':
    msg.fail("You imported unidic, but dicitionary data is not installed. "
            "Run this command to install the latest UniDic: "
            "    python -m unidic download",
            exits=1)
