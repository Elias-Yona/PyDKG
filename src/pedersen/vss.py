import secrets
from numpy.polynomial import Polynomial as Poly


class Polynomial:
    def __init__(self, degree):
        self.degree = degree

    def coefficients(self):
        c = list({secrets.SystemRandom().random()
                 for _ in range(self.degree+1)})
        secrets.SystemRandom().shuffle(c)
        return c

    def equation(self):
        c = self.coefficients()
        return Poly(self.coefficients())


degree = 5  # polynomial degree
polynomial_1 = Polynomial(degree).equation()
polynomial_2 = Polynomial(degree).equation()

print(polynomial_1)
print(polynomial_2)
