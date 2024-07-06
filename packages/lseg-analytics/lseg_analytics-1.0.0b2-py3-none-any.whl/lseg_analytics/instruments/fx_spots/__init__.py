"""FxSpot module"""

from .functions import *
from .functions import __all__ as functions_all
from .fx_spot import FxSpot

__all__ = ["FxSpot"]
__all__.extend(functions_all)

_main_class = FxSpot
