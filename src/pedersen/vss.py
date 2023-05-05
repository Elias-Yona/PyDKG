from generate_groups import CyclicGroup
from polynomials import Polynomial

group = CyclicGroup(20)


class Vss:
    def __init__(self, C):
        self.C = C

    @classmethod
    def get_commitment(cls, p, g, h, t):
        """Compute the commitments for a DKG"""
        a = Polynomial(t).coefficients()
        b = Polynomial(t).coefficients()
        C = [pow(g, int(a[k]*10), p) * pow(h, int(b[k]*10), p) %
             p for k in range(t+1)]
        return cls(C)


p = group.p
h = group.h
g = group.g
t = 10

# pedersen_vss = Vss.get_commitment(p=p, g=g, h=h, t=t)
# print(pedersen_vss.C)
