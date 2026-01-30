import math
from typing import List
from .core import PolynomialRootsBase, Root

class CubicRoots(PolynomialRootsBase):
    """
    Stable cubic solver (pure Python) handling:
    - Three distinct real roots
    - One real + two complex roots
    - Double or triple roots
    Works with frozen Root dataclass.
    """

    def __init__(self, coeffs: List[complex], **kwargs):
        super().__init__(coeffs, **kwargs)
        if len(coeffs) != 4:
            raise ValueError("Cubic polynomial requires exactly 4 coefficients [a, b, c, d]")
        self.a, self.b, self.c, self.d = self.coeffs

    def roots(self) -> List[Root]:
        if abs(self.a) < self.eps:
            raise ValueError("Leading coefficient is effectively zero")

        # Normalize cubic: x^3 + p x^2 + q x + r = 0
        p = self.b / self.a
        q = self.c / self.a
        r = self.d / self.a
        shift = -p / 3

        def is_real(z: complex) -> bool:
            return abs(z.imag) < self.eps

        real_coeffs = all(is_real(z) for z in (p, q, r))

        # Depressed cubic: t^3 + a t + b = 0
        a = q - p**2 / 3
        b = 2 * p**3 / 27 - p * q / 3 + r
        roots: List[Root] = []

        if real_coeffs:
            a = a.real
            b = b.real
            delta = (b / 2)**2 + (a / 3)**3

            def real_cbrt(x: float) -> float:
                return math.copysign(abs(x)**(1/3), x)

            if delta > self.eps:
                # One real root + complex conjugate pair
                sqrt_delta = math.sqrt(delta)
                u = real_cbrt(-b/2 + sqrt_delta)
                v = real_cbrt(-b/2 - sqrt_delta)
                t1 = u + v
                roots.append(Root(value=complex(t1 + shift.real, 0), multiplicity=1))
                re = -t1 / 2 + shift.real
                im = math.sqrt(3)/2 * abs(u - v)
                roots.append(Root(value=complex(re, im), multiplicity=1))
                roots.append(Root(value=complex(re, -im), multiplicity=1))

            elif delta < -self.eps:
                # Three distinct real roots
                rho = 2 * math.sqrt(-a / 3)
                cos_theta = (-b / 2) / math.sqrt(-(a / 3)**3)
                cos_theta = max(-1.0, min(1.0, cos_theta))
                theta = math.acos(cos_theta)
                t_vals = [rho * math.cos((theta + 2 * math.pi * k)/3) for k in range(3)]
                roots = [Root(value=complex(t + shift.real, 0), multiplicity=1) for t in t_vals]

            else:
                # delta ≈ 0 → one double root + one single root, or triple root
                if abs(b) < self.eps and abs(a) < self.eps:
                    # Triple root at shift
                    roots = [Root(value=complex(shift.real, 0), multiplicity=3)]
                else:
                    # One double root t2 = t3, one single root t1
                    u = real_cbrt(-b/2)
                    t1 = 2*u
                    t2 = -u
                    roots.append(Root(value=complex(t1 + shift.real, 0), multiplicity=1))
                    roots.append(Root(value=complex(t2 + shift.real, 0), multiplicity=2))

        else:
            # Complex coefficients: full Cardano formula
            import cmath
            def cbrt(z: complex) -> complex:
                r, phi = cmath.polar(z)
                return cmath.rect(r ** (1/3), phi / 3)
            delta = (b / 2)**2 + (a / 3)**3
            sqrt_delta = cmath.sqrt(delta)
            u = cbrt(-b/2 + sqrt_delta)
            v = cbrt(-b/2 - sqrt_delta)
            omega = cmath.exp(2j * math.pi / 3)
            omega2 = cmath.exp(4j * math.pi / 3)
            t1 = u + v
            t2 = omega * u + omega2 * v
            t3 = omega2 * u + omega * v
            roots.extend([
                Root(value=t1 + shift, multiplicity=1),
                Root(value=t2 + shift, multiplicity=1),
                Root(value=t3 + shift, multiplicity=1),
            ])

        # Merge very close roots for multiplicities (works with frozen Root)
        # if real_coeffs:
        #     roots.sort(key=lambda r: (r.value.real, r.value.imag))
        #     merged: List[Root] = []
        #     for r in roots:
        #         if merged:
        #             last = merged[-1]
        #             if abs(last.value.real - r.value.real) < self.eps and abs(last.value.imag - r.value.imag) < self.eps:
        #                 merged[-1] = Root(value=last.value, multiplicity=last.multiplicity + r.multiplicity)
        #                 continue
        #         merged.append(r)
        #     roots = merged

        # return roots
        return self._merge_roots(roots)
