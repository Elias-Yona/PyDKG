from numpy.polynomial import Polynomial as Poly
i = 2
coeffs = [0, 1, 2]
zero = 0

p = sum((coeff * (i ** j) for j, coeff in enumerate(coeffs)), zero)

print(p)


q = Poly(coeffs)

print(q(2))
