from ._version import __version__
from .quadratic import QuadraticRoots
from .cubic import CubicRoots
from .utils import format_polynomial, format_roots


__all__ = [
    "QuadraticRoots",
    "CubicRoots",
    "format_polynomial",
    "format_roots",
    "__version__",
]

