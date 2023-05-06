from functools import cached_property
from collections import defaultdict

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
        self.complaints = defaultdict(int)
        self.disqualified = set()

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
            return False

        return True

    def broadcast_complaint(self, i):
        self.complaints[i] += 1

    def get_complaints(self, i):
        return self.complaints[i]

    def handle_complaint(self, i, s_ij, s_pij, C, g, h, p):
        if i in self.disqualified:
            print(f"Player {i} is already disqualified")
            return False

        if self.get_complaints(i) >= self.degree:
            print(f"Player {i} has been banned from the game")
            self.disqualified.add(i)
            return False

        if not self.verify_share(s_ij, s_pij, C, i, g, h, p):
            self.broadcast_complaint(i)
            print(f"Player {i} received a complaint")
            self.complaints[i] += 1

            if self.get_complaints(i) >= self.degree:
                print(f"Player {i} has been banned from the game")
                self.disqualified.add(i)

            return False

        return True

    def get_non_disqualified_players(self, n):
        """Get a set of all non-disqualified players"""
        return set(range(1, n+1)) - self.disqualified

    def compute_share_xi(self, s_ij, players, q):
        """Compute the share xi for player i"""
        xi = 0
        for j in players:
            p = pow(j, s_ij)
            xi += p
        return xi % q

    def compute_share_xi_prime(self, sp_ij, players, q):
        """Compute the share xi_prime for player i"""
        xi_prime = 0
        for j in players:
            p = pow(j, sp_ij)
            xi_prime += p
        return xi_prime % q


p = group.p
h = group.h
g = group.g
t = 5
n = 5

# Initialize the dealer
dealer = Vss(degree=t)

# Generate the commitment
C = dealer.get_commitment(p=p, g=g, h=h)

# Generate shares for n players
shares = dealer.get_shares(n, p)

j = 2
for i in range(1, n + 1):
    if i == 2:
        continue
    s_ij, sp_ij = shares[i - 1]

    if i == 3:
        s_ij = 10

    is_verified = dealer.verify_share(
        s_ij=s_ij, sp_ij=sp_ij, C_j=C, g=g, h=h, p=p,  j=i)

    if not is_verified:
        dealer.broadcast_complaint(i)
        print(f"Player {j} broadcasts a complaint against Player {i}")
        dealer.handle_complaint(
            i=i, s_ij=s_ij, s_pij=sp_ij, C=C, g=g, h=h, p=p)

# compute x_i
# compute x1
s_ij0, s_pij0 = shares[0]
non_disqualified_players = dealer.get_non_disqualified_players(n)
x1 = dealer.compute_share_xi(s_ij=s_ij0, players=non_disqualified_players, q=p)
print(f'x1 => {x1}')

# compute x2
s_ij1, s_pij1 = shares[1]
non_disqualified_players = dealer.get_non_disqualified_players(n)
x2 = dealer.compute_share_xi(s_ij=s_ij1, players=non_disqualified_players, q=p)
print(f'x2 => {x2}')

# compute xi_prime
# compute x1'
s_ij0, s_pij0 = shares[0]
non_disqualified_players = dealer.get_non_disqualified_players(n)
x1_prime = dealer.compute_share_xi_prime(
    sp_ij=s_pij0, players=non_disqualified_players, q=p)
print(f'x1 prime=> {x1_prime}')

# compute x2'
s_ij1, s_pij1 = shares[1]
non_disqualified_players = dealer.get_non_disqualified_players(n)
x2_prime = dealer.compute_share_xi_prime(
    sp_ij=s_pij1, players=non_disqualified_players, q=p)
print(f'x2 prime => {x2_prime}')
