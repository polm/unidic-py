import requests
import shutil
import zipfile
import os
import sys
import time
from wasabi import msg
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
        self.update(b * bsize - self.n)

def download_file_with_resume(url, fname):
    """Download a file with resume support.

    This will download the file from the url and save it to the fname. If the
    file already exists, it will resume the download from where it left off.
    """
    existing_size = 0
    if os.path.exists(fname):
        existing_size = os.path.getsize(fname)
    
    headers = {}
    if existing_size:
        headers['Range'] = f'bytes={existing_size}-'
    
    mode = 'ab' if existing_size else 'wb'
    retries = 3
    attempt = 0
    
    while attempt < retries:
        try:
            with requests.get(url, headers=headers, stream=True, timeout=30) as r:
                r.raise_for_status()
                
                total_size = int(r.headers.get('content-length', 0))
                if existing_size and r.status_code == 206:
                    total_size += existing_size
                
                with open(fname, mode) as f:
                    with tqdm(
                        total=total_size,
                        initial=existing_size,
                        unit='B',
                        unit_scale=True,
                        miniters=1,
                        desc=url.split('/')[-1]
                    ) as pbar:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
                return fname
                
        except (requests.exceptions.RequestException, ConnectionError) as e:
            attempt += 1
            if attempt < retries:
                existing_size = os.path.getsize(fname)
                headers['Range'] = f'bytes={existing_size}-'
                time.sleep(5)
            else:
                raise
    
    return fname

def validate_zip_file(fname):
    try:
        with zipfile.ZipFile(fname, 'r') as zf:
            if zf.testzip() is not None:
                return False
        return True
    except zipfile.BadZipFile:
        return False

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
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            download_file_with_resume(url, fname)
            if validate_zip_file(fname):
                print("Download completed successfully.")
                break
            else:
                print("Downloaded file is corrupt, retrying...")
                os.remove(fname)
        except Exception as e:
            print(f"Download failed (attempt {attempt+1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(5)
                if os.path.exists(fname):
                    os.remove(fname)
            else:
                raise RuntimeError("Failed to download valid file after multiple attempts")
    
    print("Extracting archive...")
    with zipfile.ZipFile(fname, 'r') as zf:
        zf.extractall(cdir)
    os.remove(fname)

    dicdir = os.path.join(cdir, 'dicdir')
    if os.path.isdir(dicdir):
        shutil.rmtree(dicdir)

    outdir = os.path.join(cdir, dirname)
    if os.path.exists(outdir):
        shutil.move(outdir, dicdir)
    else:
        raise FileNotFoundError(f"Extracted directory not found: {outdir}")

    for dfile in delfiles:
        file_path = os.path.join(dicdir, dfile)
        if os.path.exists(file_path):
            os.remove(file_path)

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
