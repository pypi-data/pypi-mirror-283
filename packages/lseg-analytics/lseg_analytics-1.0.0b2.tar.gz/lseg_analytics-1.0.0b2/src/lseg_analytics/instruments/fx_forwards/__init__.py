"""FxForward module"""

from .functions import *
from .functions import __all__ as functions_all
from .fx_forward import FxForward

__all__ = ["FxForward"]
__all__.extend(functions_all)

_main_class = FxForward
