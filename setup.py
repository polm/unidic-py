import pathlib
import setuptools
from distutils.core import setup
import os

setup(name='unidic', 
      version='1.0.1',
      author="Paul O'Leary McCann",
      author_email="polm@dampfkraft.com",
      description="UniDic packaged for Python",
      long_description=pathlib.Path('README.md').read_text('utf8'),
      long_description_content_type="text/markdown",
      url="https://github.com/polm/unidic-py",
      packages=setuptools.find_packages(),
      package_data={'unidic': ['dicdir/*']},
      )
