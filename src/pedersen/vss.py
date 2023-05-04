import secrets
from numpy.polynomial import Polynomial as Poly


class Polynomial:
    def __init__(self, degree):
        self._degree = degree

    def coefficients(self):
        c = list({secrets.SystemRandom().random()
                 for _ in range(self._degree+1)})
        secrets.SystemRandom().shuffle(c)
        return c

    def equation(self):
        return Poly(self.coefficients())

    def __len__(self):
        return len(self.coefficients)

    def __getitem__(self, idx):
        return self.coefficients()[idx]


degree = 5  # polynomial degree
polynomial1 = Polynomial(degree).equation()
polynomial2 = Polynomial(degree).equation()

random_value1 = polynomial1(0)
random_value2 = polynomial2(0)

print(random_value1)
print(random_value2)
print(polynomial1[0])
