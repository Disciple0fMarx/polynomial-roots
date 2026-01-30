import math
import cmath
from typing import List
from .core import PolynomialRootsBase, Root


class QuarticRoots(PolynomialRootsBase):
    """
    Exact quartic solver using Ferrari's method.
    Handles:
    - Four real roots (distinct, double, triple, quadruple)
    - Two real + two complex roots
    - Four complex roots
    Works with frozen Root dataclass and automatically merges repeated roots.
    """

    def __init__(self, coeffs: List[complex], **kwargs):
        super().__init__(coeffs, **kwargs)
        if len(coeffs) != 5:
            raise ValueError("Quartic polynomial requires exactly 5 coefficients [a, b, c, d, e]")
        self.a, self.b, self.c, self.d, self.e = self.coeffs

    def roots(self) -> List[Root]:
        if abs(self.a) < self.eps:
            raise ValueError("Leading coefficient is effectively zero")

        # Normalize to monic: x^4 + p x^3 + q x^2 + r x + s = 0
        p = self.b / self.a
        q = self.c / self.a
        r = self.d / self.a
        s = self.e / self.a

        # Depressed quartic: x = y - p/4
        shift = -p / 4

        # Ferrari's method requires solving the resolvent cubic
        # y^4 + a y^3 + b y^2 + c y + d = 0  -> t^3 - (q/2) t^2 - (s) t + (...) = 0
        # Standard approach:
        # Solve cubic resolvent: z^3 - (q/2) z^2 - s z + ((4*q*s - r^2 - q^2*s)/8) = 0

        # For exact derivation, see https://en.wikipedia.org/wiki/Quartic_function#Ferrari's_solution
        # Here we implement the standard method

        # Coefficients of depressed quartic: y^4 + alpha y^2 + beta y + gamma = 0
        alpha = q - 3 * p**2 / 8
        beta = r + p**3 / 8 - p*q/2
        gamma = s - 3*p**4/256 + p**2*q/16 - p*r/4

        roots: List[Root] = []

        # Handle special case: beta == 0 -> biquadratic
        if abs(beta) < self.eps:
            # y^4 + alpha y^2 + gamma = 0 -> quadratic in y^2
            disc = alpha**2 - 4*gamma
            sqrt_disc = cmath.sqrt(disc)
            y1 = cmath.sqrt((-alpha + sqrt_disc)/2)
            y2 = cmath.sqrt((-alpha - sqrt_disc)/2)
            candidates = [y1, -y1, y2, -y2]
            for y in candidates:
                roots.append(Root(value=y + shift))
        else:
            # General Ferrari method
            # Solve resolvent cubic: z^3 - (alpha/2) z^2 - gamma z + (gamma*alpha/2 - beta^2/8) = 0
            # Coefficients: z^3 + c2 z^2 + c1 z + c0
            c2 = -alpha/2
            c1 = -gamma
            c0 = (gamma*alpha/2 - beta**2/8)

            # Solve cubic using the cubic solver method
            from .cubic import CubicRoots
            cubic = CubicRoots([1, c2, c1, c0])
            z_solutions = cubic.roots()
            # Choose one real root (or the first if complex)
            for z_root in z_solutions:
                u = z_root.value
                if abs(u.imag) < self.eps or True:
                    break

            # Compute the two quadratic factors
            sqrt1 = cmath.sqrt(2*u - alpha)
            if abs(sqrt1) < self.eps:
                # Avoid division by zero
                sqrt1 = 0
                plus_term = cmath.sqrt(u**2 - gamma)
                quad1 = [shift + (u + plus_term)/2, shift + (u - plus_term)/2]
                quad2 = [shift + (-u + plus_term)/2, shift + (-u - plus_term)/2]
            else:
                quad1 = [
                    shift + (-sqrt1 - cmath.sqrt(-(3*alpha + 2*u + 2*beta/sqrt1)))/2,
                    shift + (-sqrt1 + cmath.sqrt(-(3*alpha + 2*u + 2*beta/sqrt1)))/2,
                ]
                quad2 = [
                    shift + (sqrt1 - cmath.sqrt(-(3*alpha + 2*u - 2*beta/sqrt1)))/2,
                    shift + (sqrt1 + cmath.sqrt(-(3*alpha + 2*u - 2*beta/sqrt1)))/2,
                ]
            for y in quad1 + quad2:
                roots.append(Root(value=y))

        # Merge numerically equal roots for multiplicities
        return self._merge_roots(roots)
