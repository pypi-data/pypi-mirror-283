[affectlog: Trustworthy AI in Python](http://affectlog.com/python)

[![Python-check](https://github.com/AffectLog360/AffectLog/workflows/Python-check/badge.svg)](https://github.com/AffectLog360/AffectLog/actions?query=workflow%3APython-check)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/affectlog.svg)](https://pypi.org/project/affectlog/)
[![PyPI version](https://badge.fury.io/py/affectlog.svg)](https://badge.fury.io/py/affectlog)
[![Downloads](https://pepy.tech/badge/affectlog)](https://pepy.tech/project/affectlog)

## Overview

Unverified black box models are prone to failure. Opaqueness leads to distrust, which in turn leads to ignorance and ultimately rejection.

The `affectlog` package xrays any model, helping to explore and explain its behavior, and aiding in understanding how complex models function. The main `Explainer` object creates a wrapper around a predictive model. Wrapped models can then be explored and compared with a collection of model-level and predict-level explanations. Additionally, there are fairness methods and interactive exploration dashboards available to users.

[![](https://raw.githubusercontent.com/AffectLog360/AffectLog-docs/master/affectlog/affectlog-diagram.png)](http://python.affectlog.com/)

## Installation

The `affectlog` package is available on [PyPI](https://pypi.org/project/affectlog/) and [conda-forge](https://anaconda.org/conda-forge/affectlog).

```console
pip install affectlog -U

conda install -c conda-forge affectlog

You can install optional dependencies for all additional features using:
pip install affectlog[full]

## Examples

Introduction to the affectlog package:
SkillsAI: tutorial and examples

Key features explained: SkillsAI: explain default vs tuned model with affectlog
How to use affectlog with: xgboost, tensorflow, h2o (feat. autokeras, catboost, lightgbm)
More explanations: residuals, shap, lime
Introduction to the Fairness module in affectlog
Tutorial on bias detection with affectlog
Introduction to the Aspect module in affectlog
Introduction to the AL360 module in affectlog
AL360 documentation: Getting Started & Demos
Code in the form of jupyter notebook

## Plots

This package uses plotly to render the plots:

Install extensions to use plotly in JupyterLab: Getting Started Troubleshooting
Use show=False parameter in plot method to return plotly Figure object
It is possible to edit the figures and save them

## Citation
If you use affectlog, please cite our research:
Research- AffectLog360°. (n.d.). AffectLog. Retrieved from https://affectlog.com/research.html

## Developer
There is a detailed instruction on how to add native support for a new model/framework into affectlog, and how to add a new explanation method.
```
