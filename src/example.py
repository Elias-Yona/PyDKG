from pedersen import Vss
from pedersen import CyclicGroup

group = CyclicGroup(20)

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


iv = iv = b'\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF\x00'
# compute x_i
# compute x1
s_ij0, s_pij0 = shares[0]
non_disqualified_players = dealer.get_non_disqualified_players(n)
key = b'supersecretkey00'
x1 = dealer.compute_share_xi(
    s_ij=s_ij0, players=non_disqualified_players, q=p, key=key, iv=iv)
print(f'x1 => {x1}')

# compute x2
s_ij1, s_pij1 = shares[1]
non_disqualified_players = dealer.get_non_disqualified_players(n)
key = b'supersecretkey01'
x2 = dealer.compute_share_xi(
    s_ij=s_ij1, players=non_disqualified_players, q=p, key=key, iv=iv)
print(f'x2 => {x2}')

# compute xi_prime
# compute x1'
s_ij0, s_pij0 = shares[0]
non_disqualified_players = dealer.get_non_disqualified_players(n)
key = b'supersecretkey03'
x1_prime = dealer.compute_share_xi_prime(
    sp_ij=s_pij0, players=non_disqualified_players, q=p, key=key, iv=iv)
print(f'x1 prime=> {x1_prime}')

# compute x2'
s_ij1, s_pij1 = shares[1]
non_disqualified_players = dealer.get_non_disqualified_players(n)
key = b'supersecretkey04'
x2_prime = dealer.compute_share_xi_prime(
    sp_ij=s_pij1, players=non_disqualified_players, q=p, key=key, iv=iv)
print(f'x2 prime => {x2_prime}')

encrypted_x2 = dealer.decrypt_share(key=key, iv=iv, ciphertext=x2_prime)
print(encrypted_x2)
