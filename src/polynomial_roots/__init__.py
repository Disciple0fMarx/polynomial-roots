from ._version import __version__
from .quadratic import QuadraticRoots
from .cubic import CubicRoots
from .quartic import QuarticRoots
from .utils import format_polynomial, format_roots


__all__ = [
    "QuadraticRoots",
    "CubicRoots",
    "QuarticRoots",
    "format_polynomial",
    "format_roots",
    "__version__",
]

