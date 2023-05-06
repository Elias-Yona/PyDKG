from functools import cached_property

from utils import get_modulus
from generate_groups import CyclicGroup
from polynomials import Polynomial


group = CyclicGroup(20)


class Vss:
    def __init__(self, degree, C=None, ):
        self.C = C
        self.degree = degree
        self.q = get_modulus(degree)
        self.f = Polynomial(self.degree)
        self.fp = Polynomial(self.degree)

    @cached_property
    def equations(self):
        a = self.f.coefficients
        b = self.fp.coefficients
        print(f'a = {a}\nb = {b}')
        f = self.f.equation()
        fp = self.fp.equation()
        print(f'f = {f}\nfp = {fp}')
        return (f, fp)

    def get_commitment(self, p, g, h):
        """Compute the commitments for a DKG"""
        a = self.f.coefficients
        b = self.fp.coefficients

        commitments = []
        for k in range(self.degree):
            C = pow(g, a[k]) * pow(h, b[k])
            commitments.append(C % p)

        return commitments

    def get_shares(self, n, p):
        shares = []
        for j in range(1, n+1):
            s_ij = self.f.equation()(j)
            sp_ij = self.fp.equation()(j) % p
            shares.append([s_ij, sp_ij])

        return shares

    def verify_share(self, s_ij, sp_ij, C_j, j, g, h, p):
        # Compute the left-hand side of the equation
        lhs = (pow(g, int(s_ij), p) * pow(h, int(sp_ij), p)) % p

        # Compute the right-hand side of the equation
        rhs = 1
        for k in range(len(C_j)):
            rhs *= pow(int(C_j[k]), pow(j, k), p) % p

        print(f'lhs={lhs}\nrhs={rhs % p}')

        # Check if the two sides are equal
        if lhs != rhs % p:
            print(f"Player {j} sent an invalid share")
            return False

        return True


p = group.p
h = group.h
g = group.g
t = 5
n = 5

# Initialize the dealer
dealer = Vss(degree=t)

# Generate the commitment
C = dealer.get_commitment(p=p, g=g, h=h)

print(C)

# Generate shares for n players
shares = dealer.get_shares(n, p)

print(shares)

player0 = shares[0]
s_ij0, sp_ij0 = player0

j = 2
for i in range(1, n + 1):
    s_ij, sp_ij = shares[i - 1]
    is_verified = dealer.verify_share(
        s_ij=s_ij, sp_ij=sp_ij, C_j=C, g=g, h=h, p=p,  j=j)

    print(f'{i} => {is_verified}')
