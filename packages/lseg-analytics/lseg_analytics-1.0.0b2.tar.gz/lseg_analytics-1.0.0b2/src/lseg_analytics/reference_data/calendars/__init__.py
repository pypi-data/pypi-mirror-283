"""Calendar module"""

from .calendar import Calendar
from .functions import *
from .functions import __all__ as functions_all

__all__ = ["Calendar"]
__all__.extend(functions_all)

_main_class = Calendar
