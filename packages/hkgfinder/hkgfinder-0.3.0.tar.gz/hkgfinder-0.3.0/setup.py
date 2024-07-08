# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hkgfinder']

package_data = \
{'': ['*']}

install_requires = \
['bio>=1.3.9,<2.0.0',
 'pyfastx>=0.8.4,<0.9.0',
 'pyhmmer>=0.8.0,<0.9.0',
 'pyrodigal>=2.1.0,<3.0.0',
 'xphyle>=4.4.2,<5.0.0']

entry_points = \
{'console_scripts': ['hkgfinder = hkgfinder.hkgfinder:main']}

setup_kwargs = {
    'name': 'hkgfinder',
    'version': '0.3.0',
    'description': 'find housekeeping genes in prokaryotic (meta)genomic data',
    'long_description': "# hkgfinder\n\n*Find housekeeping genes in prokaryotic (meta)genomes*\n\n[![PyPI](https://img.shields.io/pypi/v/hkgfinder.svg)](https://pypi.org/project/hkgfinder)\n[![Wheel](https://img.shields.io/pypi/wheel/hkgfinder.svg)](https://pypi.org/project/hkgfinder)\n[![Language](https://img.shields.io/pypi/implementation/hkgfinder)](https://pypi.org/project/hkgfinder)\n[![Pyver](https://img.shields.io/pypi/pyversions/hkgfinder.svg)](https://pypi.org/project/hkgfinder)\n[![Downloads](https://img.shields.io/pypi/dm/hkgfinder)](https://pypi.org/project/hkgfinder)\n[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://www.gnu.org/licenses/MIT)\n\n\n\n\n## 🗺️ Overview\nhkgfinder is a fast and accurate housekeeping gene finder and classifier. hkgfinder can run on raw sequences, genomes and metagenomes. The novel value of this method lies is in its ability to directly predict and classify gene sequences into housekeeping gene families at a high specificity and sensitivity, while being also faster than genome and metagenome annotator on genome and metagenome data.\n\n\n## How hkgfinder works\n![](img/hkgfinder.png)\n\n## 🔧 Installing\n\nhkgfinder can be installed directly from [PyPI](https://pypi.org/project/hkgfinder).\n\n```console\n$ pip install hkgfinder\n```\n\n## Test\n\n* Type `hkgfinder -h` and it should output something like:\n\n```\nusage: hkgfinder [options] [<FILE>]\n\noptions:\n  -o [FILE]      output result to FILE [stdout]\n  -g             activate genome mode [false]\n  -m             activate metagenome mode [false]\n  --faa FILE     output matched protein sequences to FILE [false]\n  --fna FILE     output matched DNA sequences to FILE [false]\n  -s             output sequences in file by gene [false]\n  -t INT         number of threads [1]\n  -q             decrease program verbosity\n  -d             enable debug mode\n  -v, --version  show program's version number and exit\n  -h, --help     show this help message and exit\n```\n\n\n## Invoking hkgfinder\n\n```\nhkgfinder --faa housekeeping.faa --fna housekeeping.fna file.fa.gz\n```\n\n* hkgfinder supports gzip, lzma, bz2 and zstd compressed files.\n  \n## ⚠️ Issue Tracker\n\nFound a bug ? Have an enhancement request ? Head over to the [Issue Tracker](https://github.com/Ebedthan/hkgfinder/issues) if you need to report\nor ask something. If you are filing in on a bug, please include as much\ninformation as you can about the issue, and try to recreate the same bug\nin a simple, easily reproducible situation.\n\n\n## ⚖️ License\n\n[MIT](https://github.com/Ebedthan/hkgfinder/blob/main/LICENSE).\n\n\n## Author\n\n* [Anicet Ebou](https://orcid.org/0000-0003-4005-177X)\n\n",
    'author': 'Anicet Ebou',
    'author_email': 'anicet.ebou@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Ebedthan/hkgfinder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
