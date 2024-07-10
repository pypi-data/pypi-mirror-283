# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ctube']

package_data = \
{'': ['*']}

install_requires = \
['eyed3>=0.9.7,<0.10.0',
 'innertube>=2.1.16,<3.0.0',
 'pathvalidate>=3.2.0,<4.0.0',
 'pydub>=0.25.1,<0.26.0',
 'pytubefix>=5.4.2,<6.0.0',
 'requests>=2.32.2,<3.0.0']

entry_points = \
{'console_scripts': ['ctube = ctube.cli:main']}

setup_kwargs = {
    'name': 'ctube',
    'version': '0.1.7',
    'description': '',
    'long_description': '# ctube\n![Version](https://img.shields.io/badge/version-0.1.7-blue)\n[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://en.wikipedia.org/wiki/MIT_License)\n\n---\nctube is a simple program for downloading music. Written in Python, ctube has a command line interface.\\\nDownload in mp3 at the highest quality available. Metadata is automatically embedded in files (including cover art).\\\nType help for more information about the available commands and how they work.\n\n### installation\n```shell\npip install ctube\n```\n\n### usage\nto run ctube just type ctube in the terminal and press enter.\n\n---\n<p align="center">\n    <img src=".github/ctube.gif" alt="ctube.gif">\n</p>\n\n---\n\nThe program is in a stable state, however some features are missing such as:\n- better artist search.\n- configuration via file.\n- better display of download status.\n- possibility to choose the metadata to embed.\n- possibility to choose the file format and other audio parameters.\n\n---\nTested on Arch Linux:\n- alacritty 0.13.2\n- python 3.12.3\n',
    'author': 'Simone Gentili',
    'author_email': 'gensydev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/ctube/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
