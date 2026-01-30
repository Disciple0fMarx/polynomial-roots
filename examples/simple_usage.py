# from polynomial_roots import QuadraticRoots, format_polynomial, format_roots
from polynomial_roots import (
    QuadraticRoots,
    CubicRoots,
    format_polynomial,
    format_roots,
)

# x^2 - 5x + 6
p1 = QuadraticRoots([1, -5, 6])
print("Polynomial:", format_polynomial(p1.coeffs))
print("Roots:", format_roots(p1.roots()))

# x^2 + 1 = 0
p2 = QuadraticRoots([1, 0, 1], complex_output=True)
print("\nPolynomial:", format_polynomial(p2.coeffs))
print("Roots:", format_roots(p2.roots()))

# (0+4j)x^2 - (3+5j)x
p3 = QuadraticRoots([(0+4j), -(3+5j), 0], complex_output=True)
print("\nPolynomial:", format_polynomial(p3.coeffs))
print("Roots:", format_roots(p3.roots()))

# 5x^2 + (-2j)x + 13
p4 = QuadraticRoots([5, (0-2j), 13], complex_output=True)
print("\nPolynomial:", format_polynomial(p4.coeffs))
print("Roots:", format_roots(p4.roots()))

# x^3 - 6x^2 + 11x - 6 = 0  → roots: 1, 2, 3
p5 = CubicRoots([1, -6, 11, -6])
print("\nPolynomial:", format_polynomial(p5.coeffs))
print("Roots:", format_roots(p5.roots()))

# x^3 + x + 1 = 0  → one real, two complex
p6 = CubicRoots([1, 0, 1, 1], complex_output=True)
print("\nPolynomial:", format_polynomial(p6.coeffs))
print("Roots:", format_roots(p6.roots()))

# x^3 - 3x + 2 = 0  → double root at x = 1
p7 = CubicRoots([1, 0, -3, 2])
print("\nPolynomial:", format_polynomial(p7.coeffs))
print("Roots:", format_roots(p7.roots()))

# (2j)x^3 - x^2 + 4 = 0
p8 = CubicRoots([2j, -1, 0, 4], complex_output=True)
print("\nPolynomial:", format_polynomial(p8.coeffs))
print("Roots:", format_roots(p8.roots()))

# x^3 + 8 = 0  → triple real root in disguise
p9 = CubicRoots([1, 0, 0, 8])
print("\nPolynomial:", format_polynomial(p9.coeffs))
print("Roots:", format_roots(p9.roots()))
