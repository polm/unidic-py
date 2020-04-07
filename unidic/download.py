import requests
import shutil
import zipfile
import os
import sys
from wasabi import msg
from urllib.request import urlretrieve
from tqdm import tqdm

# This is used to show progress when downloading.
# see here: https://github.com/tqdm/tqdm#hooks-and-callbacks
class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""
    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize

def download_file(url, fname):
    with requests.get(url, stream=True) as r:
        with open(fname, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return fname

def download_progress(url, fname):
    """Download a file and show a progress bar."""
    with TqdmUpTo(unit='B', unit_scale=True, miniters=1,
              desc=url.split('/')[-1]) as t:  # all optional kwargs
        urlretrieve(url, filename=fname, reporthook=t.update_to, data=None)
        t.total = t.n
    return fname

def get_json(url, desc):
    r = requests.get(url)
    if r.status_code != 200:
        msg.fail(
            "Server error ({})".format(r.status_code),
            "Couldn't fetch {}. If this error persists please open an issue."
            " http://github.com/polm/unidic-py/issues/".format(desc),
            exits=1,
        )
    return r.json()

def download_and_clean(version, url, dirname='unidic', delfiles=[]):
    """Download unidic and prep the dicdir.

    This downloads the zip file from the source, extracts it, renames the
    resulting directory, and removes large files not used at runtime.  
    """
    cdir = os.path.dirname(os.path.abspath(__file__))
    cdir = os.path.join(cdir, 'unidic')
    fname = cdir + '/unidic.zip'
    print("Downloading UniDic v{}...".format(version), file=sys.stderr)
    download_progress(url, fname)
    print("Finished download.")

    with zipfile.ZipFile(fname, 'r') as zf:
        zf.extractall(cdir)
    os.remove(fname)

    dicdir = cdir + '/dicdir'
    if os.path.isdir(dicdir):
        shutil.rmtree(dicdir)

    shutil.move(cdir + '/' + dirname, dicdir)

    for dfile in delfiles:
        os.remove(dicdir + '/' + dfile)

    # save a version file so we can tell what it is
    with open(dicdir + '/version', 'w') as vfile:
        vfile.write('unidic-{}'.format(version))

    # Write a dummy mecabrc
    with open(dicdir + '/mecabrc', 'w') as mecabrc:
        mecabrc.write('# This is a dummy file.')

    print("Downloaded UniDic v{} to {}".format(version, dicdir), file=sys.stderr)

DICT_INFO = "https://raw.githubusercontent.com/polm/unidic-py/master/dicts.json"
DOWNLOAD_BASE = "https://github.com/polm/unidic-py/releases/download/"

def download_version(ver="latest"):
    res = get_json(DICT_INFO, "dictionary info")
    print(res)
    try:
        dictinfo = res[ver]
    except KeyError:
        print('Unknown version "{}".'.format(ver))
        print("Known versions:")
        for key, val in res.items():
            print("\t", key, "({})".format(val['version']))

    print("download url:", dictinfo['url'])
    print("Dictionary version:", dictinfo['version'])
    download_and_clean(dictinfo['version'], dictinfo['url'])

