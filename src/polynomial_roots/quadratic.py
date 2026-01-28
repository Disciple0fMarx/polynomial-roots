import cmath
from typing import List

from .core import PolynomialRootsBase, Root


class QuadraticRoots(PolynomialRootsBase):
    """
    Exact root finder for quadratic polynomials.
    """

    def __init__(self, coeffs: List[complex], **kwargs):
        super().__init__(coeffs, **kwargs)
        if len(coeffs) != 3:
            raise ValueError("Quadratic polynomial requires exactly 3 coefficients [a, b, c]")

        self.a, self.b, self.c = self.coeffs

    def roots(self) -> List[Root]:
        """
        Compute roots using quadratic formula.
        """
        if abs(self.a) < self.eps:
            raise ValueError("Leading coefficient is effectively zero")

        discriminant = self.b ** 2 - 4 * self.a * self.c

        roots_list = []

        if abs(discriminant) < self.eps:
            # double root
            r = -self.b / (2 * self.a)
            roots_list.append(Root(value=r, multiplicity=2))
        else:
            sqrt_d = cmath.sqrt(discriminant)

            r1 = (-self.b + sqrt_d) / (2 * self.a)
            r2 = (-self.b - sqrt_d) / (2 * self.a)

            # Clean up tiny imaginary parts if not forcing complex output
            if not self.complex_output:
                if abs(r1.imag) < self.eps:
                    r1 = complex(r1.real, 0)
                if abs(r2.imag) < self.eps:
                    r2 = complex(r2.real, 0)

            roots_list.extend([Root(value=r1), Root(value=r2)])

        return roots_list

