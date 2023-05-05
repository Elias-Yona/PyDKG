import secrets

from numpy.polynomial import Polynomial as Poly


class Polynomial():
    def __init__(self, degree: int) -> None:
        self._degree = degree

    def coefficients(self):
        c = list({secrets.SystemRandom().random()
                  for _ in range(self._degree+1)})
        secrets.SystemRandom().shuffle(c)
        return c

    def __call__(self, i):
        eq = Poly(self.coefficients())
        return eq(i)

    def __len__(self):
        return len(self.coefficients)

    def __getitem__(self, idx):
        return self.coefficients()[idx]


# degree = 5  # polynomial degree

# p1 = Polynomial(degree)
# print(p1(4))
