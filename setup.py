import pathlib
import setuptools
from distutils.core import setup

setup(name='unidic', 
      version='0.0.4',
      author="Paul O'Leary McCann",
      author_email="polm@dampfkraft.com",
      description="UniDic packaged for Python",
      long_description=pathlib.Path('README.md').read_text('utf8'),
      long_description_content_type="text/markdown",
      url="https://github.com/polm/unidic-py",
      packages=setuptools.find_packages(),
      package_data={'unidic': ['dicdir/*']}
      )
