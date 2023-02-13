import os
import shutil
import sys
import zipfile

import requests
from tqdm import tqdm
from wasabi import msg


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
    file_size = int(requests.head(url).headers["content-length"])
    response = requests.get(url, stream=True)
    progress_bar = tqdm(total=file_size, unit="B", unit_scale=True)
    with open(fname, "wb") as fp:
        for chunk in response.iter_content(chunk_size=1024**2):
            fp.write(chunk)
            progress_bar.update(len(chunk))
        progress_bar.close()

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
    fname = os.path.join(cdir, 'unidic.zip')
    print("Downloading UniDic v{}...".format(version), file=sys.stderr)
    download_progress(url, fname)
    print("Finished download.")

    with zipfile.ZipFile(fname, 'r') as zf:
        zf.extractall(cdir)
    os.remove(fname)

    dicdir = os.path.join(cdir, 'dicdir')
    if os.path.isdir(dicdir):
        shutil.rmtree(dicdir)

    outdir = os.path.join(cdir, dirname)
    shutil.move(outdir, dicdir)

    for dfile in delfiles:
        os.remove(os.path.join(dicdir, dfile))

    # save a version file so we can tell what it is
    vpath = os.path.join(dicdir, 'version')
    with open(vpath, 'w') as vfile:
        vfile.write('unidic-{}'.format(version))

    # Write a dummy mecabrc
    with open(os.path.join(dicdir, 'mecabrc'), 'w') as mecabrc:
        mecabrc.write('# This is a dummy file.')

    print("Downloaded UniDic v{} to {}".format(version, dicdir), file=sys.stderr)

DICT_INFO = "https://raw.githubusercontent.com/polm/unidic-py/master/dicts.json"

def download_version(ver="latest"):
    res = get_json(DICT_INFO, "dictionary info")
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

