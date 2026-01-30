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
    
    def _merge_roots(self, roots: List[Root]) -> List[Root]:
        """
        Merge numerically close roots into single roots with multiplicity.
        """

        MERGE_EPS = 10 * self.eps

        # Sort roots deterministically
        roots_sorted = sorted(
            roots, key=lambda r: (r.value.real, r.value.imag)
        )

        merged: List[Root] = []

        for r in roots_sorted:
            z = r.value

            # Snap tiny imaginary parts to zero
            if abs(z.imag) < self.eps:
                z = complex(z.real, 0)

            if not merged:
                merged.append(Root(value=z, multiplicity=r.multiplicity))
                continue

            last = merged[-1]
            dz = z - last.value

            if abs(dz) < MERGE_EPS:
                # Merge: compute centroid to avoid drift (critical for (x-a)^4)
                total_mult = last.multiplicity + r.multiplicity
                avg = (
                    last.value * last.multiplicity + z * r.multiplicity
                ) / total_mult

                merged[-1] = Root(
                    value=avg,
                    multiplicity=total_mult,
                )
            else:
                merged.append(Root(value=z, multiplicity=r.multiplicity))

        return merged
