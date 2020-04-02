import pathlib
import setuptools
from distutils.core import setup
import os

from download import download_latest

_curdir = os.path.dirname(__file__)
DICDIR = os.path.join(_curdir, 'dicdir')

if not os.path.exists(DICDIR + '/version'):
    print("Downloading dictionary data.")
    download_latest()

# This will download the data if it's not present

setup(name='unidic', 
      version='0.0.5',
      author="Paul O'Leary McCann",
      author_email="polm@dampfkraft.com",
      description="UniDic packaged for Python",
      long_description=pathlib.Path('README.md').read_text('utf8'),
      long_description_content_type="text/markdown",
      url="https://github.com/polm/unidic-py",
      packages=setuptools.find_packages(),
      package_data={'unidic': ['dicdir/*']}
      )
