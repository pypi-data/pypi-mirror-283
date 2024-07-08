# AffectLog

[AffectLog: Trustworthy Machine Learning Assessment](http://affectLog.com/python)

[![Python-check](https://github.com/AffectLog360/AffectLog/workflows/Python-check/badge.svg)](https://github.com/AffectLog360/AffectLog/actions?query=workflow%3APython-check)
[![Supported Python
versions](https://img.shields.io/pypi/pyversions/affectlog.svg)](https://pypi.org/project/affectlog/)
[![PyPI version](https://badge.fury.io/py/affectlog.svg)](https://badge.fury.io/py/affectlog)
[![Downloads](https://pepy.tech/badge/affectlog)](https://pepy.tech/project/affectlog)

## Overview

Unverified black box models are destined for failure. Lack of transparency breeds distrust, leading to neglect and eventual rejection.

The 'affectlog' package offers a suite of tools to dissect and explain the behavior of any predictive model. The central component, the Explainer object, wraps around the model, facilitating detailed exploration and comparison through various model-level and prediction-level explanations. Additionally, 'affectlog' provides methods for assessing fairness and interactive dashboards for comprehensive analysis.

## Installation

The `affectlog` package is available on [PyPI](https://pypi.org/project/affectlog/) and [conda-forge](https://anaconda.org/conda-forge/affectlog).

```console
pip install affectlog -U

conda install -c conda-forge affectlog

One can install optional dependencies for all additional features using pip install affectlog[full].

Resources: https://affectlog.com/research.html
API reference: https://affectlog.com/research/api

## Authors
The authors of the affectlog package are:

AffectLog Developer Team
We welcome contributions: start by opening an issue on GitHub.

## Citation
If you use affectlog, please cite our research:
@article{AffectLog360,
  author  = {AffectLog Developer Team},
  title   = {AffectLog: Trustworthy Machine Learning
             with Interactive Explainability and Fairness in Python},
  journal = {Research- AffectLog360°},
  year    = {n.d.},
  url     = {https://affectlog.com/research.html}
}
```
