import requests
import shutil
import zipfile
import os
import sys
from wasabi import msg

def download_file(url, fname):
    with requests.get(url, stream=True) as r:
        with open(fname, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return fname

def get_json(url, desc):
    r = requests.get(url)
    if r.status_code != 200:
        msg.fail(
            "Server error ({})".format(r.status_code),
            "Couldn't fetch {}. If this error persists please open an issue."
            " http://github.com/polm/fugashi/issues/".format(desc),
            exits=1,
        )
    return r.json()

DICTS = {
        '2.1.2': {
            'url': 'https://unidic.ninjal.ac.jp/unidic_archive/cwj/2.1.2/unidic-mecab-2.1.2_bin.zip',
            'dirname': 'unidic-mecab-2.1.2_bin',
            'delfiles': []},
        }
        
def download_and_clean(version, url, dirname='unidic', delfiles=[]):
    """Download unidic and prep the dicdir.

    This downloads the zip file from the source, extracts it, renames the
    resulting directory, and removes large files not used at runtime.  
    """
    cdir = os.path.dirname(os.path.abspath(__file__))
    fname = cdir + '/unidic.zip'
    print("Downloading UniDic v{}...".format(version), file=sys.stderr)
    download_file(url, fname)

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

def download(version):
    if version in DICTS:
        vdata = DICTS[version]
        download_and_clean(version, vdata['url'], vdata['dirname'], vdata['delfiles'])
    else:
        print("Unknown version:", version)
        print("Available versions:", ", ".join(DICTS))
        sys.exit(1)

DICT_INFO = "https://raw.githubusercontent.com/polm/unidic-py/master/dicts.json"
DOWNLOAD_BASE = "https://github.com/polm/unidic-py/releases/download/"

def download_latest():
    res = get_json(DICT_INFO, "dictionary info")
    version = res['latest']
    vtemp = "unidic-{v}/unidic-{v}.zip"
    download_url = DOWNLOAD_BASE + vtemp.format(v=version)
    download_and_clean(version, download_url)

