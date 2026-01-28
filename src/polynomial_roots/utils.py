from typing import List

# from .core import Root


def format_polynomial(coeffs: List[complex], var: str = "x") -> str:
    """
    Create a nice string representation of the polynomial.
    """
    if not coeffs:
        return "0"
    eps = 1e-10

    terms = []
    degree = len(coeffs) - 1

    for i, c in enumerate(coeffs):
        if abs(c) < eps:
            continue
        power = degree - i

        # Constant term
        if power == 0:
            terms.append(format_complex(c))
            continue
        
        # Coefficient
        if abs(c - 1) < eps:
            coeff = ""
        elif abs(c + 1) < eps:
            coeff = "-"
        else:
            coeff = format_complex(c, parens=True)

        # Variable part
        if power == 1:
            terms.append(f"{coeff}{var}")
        else:
            terms.append(f"{coeff}{var}^{power}")

    return " + ".join(terms).replace("+ -", "- ")


def format_roots(roots) -> str:
    """
    """
    return ", ".join(str(r) for r in roots)


def format_complex(z: complex, *, parens: bool = False) -> str:
    """
    Format a complex number in a human-friendly way.
    """
    eps = 1e-10
    re = z.real if abs(z.real) > eps else 0.0
    im = z.imag if abs(z.imag) > eps else 0.0

    # Pure real
    if im == 0:
        return f"{re:.4g}"

    # Pure imaginary
    if re == 0:
        if im == 1:
            return "i"
        if im == -1:
            return "-i"
        return f"{im:.4g}i"

    # General complex
    sign = "+" if im > 0 else "-"
    im_abs = abs(im)

    if im_abs == 1:
        s = f"{re:.4g}{sign}i"
    else:
        s = f"{re:.4g}{sign}{im_abs:.4g}i"

    return f"({s})" if parens else s

