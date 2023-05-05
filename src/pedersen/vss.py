import secrets
from collections.abc import Sequence
from typing import Union

from numpy.polynomial import Polynomial as Poly

from groups import PreGroupValue


class Polynomial(Sequence[PreGroupValue]):
    def __init__(self, degree: int) -> None:
        self._degree = degree

    def coefficients(self) -> PreGroupValue:
        c = list({secrets.SystemRandom().random()
                  for _ in range(self._degree+1)})
        secrets.SystemRandom().shuffle(c)
        return c

    def __call__(self, i: int) -> PreGroupValue:
        eq = Poly(self.coefficients())
        return eq(i)

    def __len__(self) -> int:
        return len(self.coefficients)

    def __getitem__(self, idx: Union[int, slice]) -> Union[PreGroupValue, Sequence[PreGroupValue]]:
        return self.coefficients()[idx]


degree = 5  # polynomial degree

p1 = Polynomial(degree)
print(p1(4))
