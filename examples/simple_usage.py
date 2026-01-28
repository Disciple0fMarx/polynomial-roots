from polynomial_roots import QuadraticRoots, format_polynomial, format_roots

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

