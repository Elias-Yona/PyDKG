from utils import get_modulus
from generate_groups import CyclicGroup
from polynomials import Polynomial

group = CyclicGroup(20)


class Vss:
    def __init__(self, degree, C=None, ):
        self.C = C
        self.degree = degree
        self.f = Polynomial(degree)
        self.fp = Polynomial(degree)
        self.q = get_modulus(degree)

    @classmethod
    def get_commitment(cls, p, g, h, t):
        """Compute the commitments for a DKG"""
        a = Polynomial(t).coefficients()
        b = Polynomial(t).coefficients()
        C = [pow(g, int(a[k]*10), p) * pow(h, int(b[k]*10), p) %
             p for k in range(t+1)]
        return cls(C)

    def get_shares(self, n):
        shares = []
        for j in range(1, n+1):
            s_ij = self.f(j) % self.q
            sp_ij = self.fp(j) % self.q
            shares.append([s_ij, sp_ij])
        return shares


p = group.p
h = group.h
g = group.g
t = 10


# v = Vss(t)
# print(v.get_shares(5))
# pedersen_vss = Vss.get_commitment(p=p, g=g, h=h, t=t)
# print(pedersen_vss.C)
