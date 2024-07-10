"""A package for logging extras."""
from ._version import __version__
from .filters import DiffTimeFilter, RelativeTimeFilter
from .formatters import TieredFormatter
from .utils import log_function_call

try:
    from .mqtt import MQTTHandler
except ImportError:
    MQTTHandler = None  # type: ignore

__all__ = [
    'DiffTimeFilter',
    'MQTTHandler',
    'RelativeTimeFilter',
    'TieredFormatter',
    '__version__',
    'log_function_call',
]
