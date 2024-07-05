from importlib.metadata import version

from .problem_bank_helpers import *

# Keep stats as a separate namespace, but also make it accessible from the top level without an explicit import
from . import stats as stats


__version__ = version("problem_bank_helpers")
