import os

def _prep_data(dicdir):
    """Unzip dictionary data."""
    import gzip
    import shutil

    for fname in ['sys.dic', 'matrix.bin']:
        outfile = os.path.join(dicdir, fname)
        gzfile = outfile + '.gz'
        with gzip.open(gzfile, 'rb') as f_in:
            with open(outfile, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(gzfile)

_curdir = os.path.dirname(__file__)

# This will be used elsewhere to initialize the tagger
DICDIR = os.path.join(_curdir, 'dicdir')

# The first time this is imported, unzip the large data files.
if not os.path.isfile(os.path.join(DICDIR, 'sys.dic')):
    _prep_data(DICDIR)
