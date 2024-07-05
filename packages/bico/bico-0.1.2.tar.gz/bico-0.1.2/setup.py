# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bico']

package_data = \
{'': ['*'],
 'bico': ['base/*',
          'clustering/*',
          'datastructure/*',
          'evaluation/*',
          'exception/*',
          'point/*']}

install_requires = \
['numpy>=1.26.4,<2.0.0', 'scikit-learn>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'bico',
    'version': '0.1.2',
    'description': 'BICO is a fast streaming algorithm to compute coresets for the k-means problem on very large sets of points.',
    'long_description': '[![Build Status](https://github.com/algo-hhu/bico/actions/workflows/mypy-flake-test.yml/badge.svg)](https://github.com/algo-hhu/bico/actions)\n[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n[![Supported Python version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)\n[![Stable Version](https://img.shields.io/pypi/v/bico?label=stable)](https://pypi.org/project/bico/)\n\n# BICO\n\nBICO is a fast streaming algorithm to compute high quality solutions for the k-means problem on very large sets of points. It combines the tree data structure of SIGMOND Test of Time Award winning algorithm BIRCH with insights from clustering theory to obtain solutions fast while keeping the error regarding the k-means cost function low.\n\n<!---\nTODO: Add logo\n<p align="center">\n  <img src="https://raw.githubusercontent.com/algo-hhu/bico/main/images/logo.png" alt="BICO Logo"/>\n</p>\n-->\n\n## Installation\n\n```bash\npip install bico\n```\n\n## Example\n\n```python\nfrom bico import BICO\nimport numpy as np\nimport time\n\nnp.random.seed(42)\n\ndata = np.random.rand(10000, 10)\n\nstart = time.time()\nbico = BICO(n_clusters=3, random_state=0, fit_coreset=True)\nbico.fit(data)\n\nprint("Time:", time.time() - start)\n# Time: 0.08275651931762695\n\nprint(bico.coreset_points_)\n# BICO returns a set of points that act as a summary of the entire dataset.\n# By default, at most 200 * n_clusters points are returned.\n# This behaviour can be changed by setting the `summary_size` parameter.\n\n# [[0.45224018 0.70183673 0.55506671 ... 0.70132665 0.57244196 0.66789088]\n#  [0.73712952 0.5250208  0.43809322 ... 0.61427161 0.67910981 0.56207661]\n#  [0.89905336 0.46942062 0.20677639 ... 0.74210482 0.75714522 0.49651055]\n#  ...\n#  [0.68744494 0.41508081 0.39197623 ... 0.44093386 0.21983902 0.37237243]\n#  [0.60820965 0.29406341 0.67067782 ... 0.66435474 0.2390822  0.20070476]\n#  [0.67385626 0.33474823 0.68238779 ... 0.3581703  0.65646253 0.41386131]]\n\nprint(bico.cluster_centers_)\n# If the `fit_coreset` parameter is set to True, the cluster centers are computed using KMeans from sklearn based on the coreset.\n\n# [[0.46892639 0.41968333 0.47302945 0.51782955 0.39390839 0.56209413\n#   0.4481691  0.49521457 0.31394509 0.5104331 ]\n#  [0.54384638 0.518978   0.49456809 0.56677848 0.63881783 0.33627504\n#   0.49873782 0.5541338  0.52913562 0.56017203]\n#  [0.48639347 0.55542596 0.54350474 0.41931257 0.48117255 0.60089563\n#   0.55457724 0.44833238 0.67583389 0.43069267]]\n```\n\n## Example with Large Datasets\n\nFor very large datasets, the data may not actually fit in memory. In this case, you can use `partial_fit` to stream the data in chunks. In this example, we use the [US Census Data (1990) dataset](https://archive.ics.uci.edu/dataset/116/us+census+data+1990). You can find more examples in the [tests](./tests/test.py) folder.\n\n```python\nfrom bico import BICO\nimport numpy as np\nimport time\n\nnp.random.seed(42)\n\ndata = np.random.rand(10000, 10)\n\nstart = time.time()\nbico = BICO(n_clusters=3, random_state=0)\nfor chunk in pd.read_csv(\n    "census.txt", delimiter=",", header=None, chunksize=10000\n):\n    bico.partial_fit(chunk.to_numpy(copy=False))\n# If a final `partial_fit` is called with no data, the coreset is computed\nbico.partial_fit()\n```\n\n## Development\n\nInstall [poetry](https://python-poetry.org/docs/#installation)\n```bash\ncurl -sSL https://install.python-poetry.org | python3 -\n```\n\nInstall clang\n```bash\nsudo apt-get install clang\n```\n\nSet clang variables\n```bash\nexport CXX=/usr/bin/clang++\nexport CC=/usr/bin/clang\n```\n\nInstall the package\n```bash\npoetry install\n```\n\nIf the installation does not work and you do not see the C++ output, you can build the package to see the stack trace\n```bash\npoetry build\n```\n\nRun the tests\n```bash\npoetry run python -m unittest discover tests -v\n```\n\n## Citation\n\nIf you use this code, please cite [the following paper](https://link.springer.com/chapter/10.1007/978-3-642-40450-4_41):\n\n```\nHendrik Fichtenberger, Marc Gillé, Melanie Schmidt, Chris Schwiegelshohn and Christian Sohler. "BICO: BIRCH Meets Coresets for k-Means Clustering" (2013). ESA 2013.\n```\n',
    'author': 'Melanie Schmidt',
    'author_email': 'mschmidt@hhu.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}
from build_extension import *
build(setup_kwargs)

setup(**setup_kwargs)
