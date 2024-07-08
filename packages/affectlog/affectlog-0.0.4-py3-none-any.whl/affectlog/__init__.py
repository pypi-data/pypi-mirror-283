"""
.. include:: ./documentation.md
"""

from . import datasets
from .aspect import Aspect

from .al360.object import AL360
from ._explainer.object import Explainer

from .datasets._load import (
    load_DataScientist, 
    load_ds_salaries, 
    load_HR_Employee_Attrition, 
    load_Online_Courses, 
    load_Salary_Data
)

__all__ = [
    "load_DataScientist",
    "load_ds_salaries",
    "load_HR_Employee_Attrition",
    "load_Online_Courses",
    "load_Salary_Data",
    "Explainer",
    "AL360"
]

# specify autocompletion in IPython
# see comment: https://github.com/ska-telescope/katpoint/commit/ed7e8b9e389ee035073c62c2394975fe71031f88
# __dir__ docs (Python 3.7!): https://docs.python.org/3.7/library/functions.html#dir


def __dir__():
    """IPython tab completion seems to respect this."""
    return __all__ + [
        "__all__",
        "__builtins__",
        "__cached__",
        "__doc__",
        "__file__",
        "__loader__",
        "__name__",
        "__package__",
        "__path__",
        "__spec__",
        "__version__",
    ]