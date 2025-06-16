"""
Unified Concurrent Task Scheduler Library

This library provides common functionality shared across all persona implementations
of the concurrent task scheduler. It includes base models, interfaces, utilities,
and monitoring capabilities.
"""

from . import core
from . import monitoring
from . import exceptions

__version__ = "1.0.0"

__all__ = [
    'core',
    'monitoring', 
    'exceptions'
]
