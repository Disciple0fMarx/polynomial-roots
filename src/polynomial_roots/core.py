from dataclasses import dataclass
from typing import Union, List

from .utils import format_complex


@dataclass(frozen=True)
class Root:
    """
    Represents a root of a polynomial with its multiplicity.
    """
    value: complex
    multiplicity: int = 1

    def __post_init__(self):
        if self.multiplicity < 1:
            raise ValueError("Multiplicity must be positive")

    def __str__(self) -> str:
        val = format_complex(self.value)
        if self.multiplicity == 1:
            return val
        return f"{val} (multiplicity {self.multiplicity})"

    def __repr__(self) -> str:
        return f"Root(value={self.value!r}, multiplicity={self.multiplicity})"


class PolynomialRootsBase:
    """
    Base class for polynomial root finders.
    """

    def __init__(self, coeffs: List[Union[float, int, complex]], *,
                 complex_output: bool = False,
                 eps: float = 1e-10):
        self.coeffs = [complex(c) for c in coeffs]
        self.complex_output = complex_output
        self.eps = eps  # tolerance for considering imaginary part zero

        if abs(self.coeffs[0]) < eps:
            raise ValueError("Leading coefficient is effectively zero")

    def roots(self) -> List[Root]:
        """Must be implemented by subclasses."""
        raise NotImplementedError

