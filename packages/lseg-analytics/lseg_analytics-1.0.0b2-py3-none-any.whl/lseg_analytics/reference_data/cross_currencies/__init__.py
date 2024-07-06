"""CrossCurrency module"""

from .cross_currency import CrossCurrency
from .functions import *
from .functions import __all__ as functions_all

__all__ = ["CrossCurrency"]
__all__.extend(functions_all)

_main_class = CrossCurrency
