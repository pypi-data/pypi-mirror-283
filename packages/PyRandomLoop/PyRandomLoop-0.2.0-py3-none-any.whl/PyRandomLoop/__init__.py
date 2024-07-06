# PyRandomLoop/__init__.py
from .core import rpm, utils
from .core.rpm import RPM

__all__ = ['rpm', 'utils']

# Since running @jit functions for the first time is slow, we do a step of the chain at import
m = RPM(1, 10, 1)
m.step(progress_bar=False)
del m
