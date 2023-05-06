import secrets
from functools import cached_property

from numpy.polynomial import Polynomial as Poly


class Polynomial():
    def __init__(self, degree: int) -> None:
        self._degree = degree

    @cached_property
    def coefficients(self):
        # c = list({int(secrets.SystemRandom().random()*100)
        #           for _ in
        # range(self._degree+1)})

        c = []
        for i in range(1, self._degree + 1):
            r = secrets.randbelow(3) + 1
            c.append(r)

        secrets.SystemRandom().shuffle(c)
        return c

    def equation(self):
        return Poly(self.coefficients)

    def __len__(self):
        return len(self.coefficients)

    def __getitem__(self, idx):
        return self.coefficients()[idx]


# degree = 5  # polynomial degree

# p1 = Polynomial(degree)
# print(p1(4))
