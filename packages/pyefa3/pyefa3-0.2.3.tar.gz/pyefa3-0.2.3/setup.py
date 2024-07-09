from setuptools import setup

import pyefa

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='pyefa3',
      version=pyefa.__version__,
      description='Python-Bindings for online train connection APIs.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Nils Martin Klünder, Kai Anter',
      author_email='nomoketo@nomoketo.de, kai@anter.dev',
      url='https://github.com/Tanikai/pyefa3',
      packages=['pyefa'],
      license='Apache',
      classifiers=[
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'License :: OSI Approved :: Apache Software License'],
      install_requires=['beautifulsoup4', 'colorama', 'lxml'],
      )
