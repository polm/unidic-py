import requests
import shutil
import zipfile
import os
import sys

def download_file(url, fname):
    with requests.get(url, stream=True) as r:
        with open(fname, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return fname

DICTS = {
        '2.1.2': {
            'url': 'https://unidic.ninjal.ac.jp/unidic_archive/cwj/2.1.2/unidic-mecab-2.1.2_bin.zip',
            'dirname': 'unidic-mecab-2.1.2_bin',
            'delfiles': []},
        }
        
def download_and_clean(version, url, dirname, delfiles):
    """Download unidic and prep the dicdir.

    This downloads the zip file from the source, extracts it, renames the
    resulting directory, and removes large files not used at runtime.  
    """
    cdir = os.path.dirname(os.path.abspath(__file__))
    fname = cdir + '/unidic.zip'
    print("Downloading UniDic v{}...".format(version))
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

    print("Downloaded UniDic v{} to {}".format(version, dicdir))

def download(version):
    if version in DICTS:
        vdata = DICTS[version]
        download_and_clean(version, vdata['url'], vdata['dirname'], vdata['delfiles'])
    else:
        print("Unknown version:", version)
        print("Available versions:", ", ".join(DICTS))
        sys.exit(1)
