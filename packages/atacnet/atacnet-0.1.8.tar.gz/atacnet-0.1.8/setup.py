# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atacnet']

package_data = \
{'': ['*'], 'atacnet': ['pyquic/*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'numpy>=1.25.0,<2.0.0',
 'pandas>=2.1.1,<3.0.0',
 'rich>=10.12.0,<11.0.0',
 'scanpy>=1.8.1,<2.0.0',
 'scikit-learn>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'atacnet',
    'version': '0.1.8',
    'description': 'Package for building co-accessibility networks from ATAC-seq data.',
    'long_description': '<p align="center">\n  <picture>\n    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/r-trimbour/atacnet/main/logo_dark_theme.svg" width="600">\n    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/r-trimbour/atacnet/main/logo.svg" width="600">\n    <img alt="Circe logo" src="https://raw.githubusercontent.com/r-trimbour/atacnet/main/logo.svg" width="600">\n  </picture>\n</p>\n\n-----------------\n# CIRCE: Cis-regulatory interactions between chromatin regions\n[![Unit_Tests](https://github.com/r-trimbour/atacnet/actions/workflows/codecov.yaml/badge.svg)](https://github.com/r-trimbour/atacnet/actions/workflows/codecov.yaml)\n[![codecov](https://codecov.io/gh/r-trimbour/atacnet/graph/badge.svg?token=0OIFAP28D7)](https://codecov.io/gh/r-trimbour/atacnet)\n[![PyPI version](https://img.shields.io/pypi/v/atacnet?color=blue)](https://img.shields.io/pypi/v/atacnet)\n[![Downloads](https://static.pepy.tech/badge/atacnet/month)](https://pepy.tech/project/atacnet)\n\n\n## Description\nThis repo contains a python package for inferring **co-accessibility networks from single-cell ATAC-seq data**, using [skggm](https://www.github.com/skggm/skggm) for the graphical lasso and [scanpy](https://www.github.com/theislab/scanpy) for data processing.\n\nIt is based on the pipeline and hypotheses presented in the manuscript "Cicero Predicts cis-Regulatory DNA Interactions from Single-Cell Chromatin Accessibility Data" by Pliner et al. (2018). This R package [Cicero](https://cole-trapnell-lab.github.io/cicero-release/) is available [here](https://www.github.com/cole-trapnell-lab/cicero-release).\n\nResults may slitghly vary between both packages, notably due to the different implementations of graphical lasso. \n<br> Currently, scores are very close when applied to the same metacells, computed from Cicero\'s methodology. (cf comparison plots below). It should run significantly faster than Cicero _(e.g.: running time of 5 sec instead of 17 min for the dataset 2)_.\n\n_If you have any suggestion, don\'t hesitate ! This package is still a work in progress :)_\n\n\n## Installation\nThe package can be installed using pip:\n\n```\npip install atacnet\n```\n\n and from github\n```\npip install "git+https://github.com/r-trimbour/atacnet.git"\n```\n\n## Minimal example\n```\nimport anndata as ad\nimport atacnet as an\n\natac = ad.read_h5ad(\'atac_data.h5ad\')\nan.add_region_infos(atac)\nan.compute_atac_network(atac)\nan.extract_atac_links(atac)\n```\n\n## Comparison to Cicero R package\n<br> *On the same metacells obtained from Cicero code.*\n\nAll tests can be found in the [AtacNet benchmark repo](https://github.com/r-trimbour/atacnet_benchmark)\n\n### Toy dataset 1 (fake data): \n- Pearson correlation coefficient: 0.999126\n- Spearman correlation coefficient: 0.99838\n<img src="https://raw.githubusercontent.com/r-trimbour/atacnet/main/Figures/correlation_toy_dataset1.png" align="center" width="480"/>\n\n### Real dataset 2 (subsample of neurips PBMC)\n- Pearson correlation coefficient: 0.999958\n- Spearman correlation coefficient: 0.999911\n<img src="https://github.com/r-trimbour/atacnet/raw/main/Figures/correlation_real_dataset2.png" align="center" width="480"/>\n\nPerformance on real dataset 2:\n- Runtime: ~100x faster\n- Memory usage: ~5x less\n<img src="https://github.com/r-trimbour/atacnet/raw/main/Figures/perf_real_dataset2.png" align="center" width="480"/>\n\n### Coming:\n\n- _**Calculate metacells !**_\n- _Add stats on similarity on large datasets._\n- _Add stats on runtime, memory usage._\n- This package can be run on multiple cores. _Currently working to speed up the mutlithreding use._\n- _Fix seed for reproducibility._\n\n## Usage\nIt is currently developped to work with AnnData objects. Check Example1.ipynb for a simple usage example.\n\n',
    'author': 'Rémi Trimbour',
    'author_email': 'remi.trimbour@pasteur.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.13',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
