from functools import cached_property
from collections import defaultdict

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64

from .utils import get_modulus
from .polynomials import Polynomial


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

    def compute_share_xi(self, s_ij, players, q, key, iv):
        """Compute the share xi for player i"""
        xi = 0
        for j in players:
            p = pow(j, s_ij)
            xi += p
        plaintext = bytes(str(xi % q), encoding='utf-8')
        return self.encrypt_share(key=key, iv=iv, plaintext=plaintext)

    def compute_share_xi_prime(self, sp_ij, players, q, key, iv):
        """Compute the share xi_prime for player i"""
        xi_prime = 0
        for j in players:
            p = pow(j, sp_ij)
            xi_prime += p

        plaintext = bytes(str(xi_prime % q), encoding='utf-8')
        return self.encrypt_share(key=key, iv=iv, plaintext=plaintext)

    def encrypt_share(self, key, iv, plaintext):
        block_size = 16
        padding_length = block_size - len(plaintext) % block_size
        padding = bytes([padding_length]) * padding_length
        padded_message = plaintext + padding
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_message) + encryptor.finalize()
        return base64.b64encode(ciphertext,)

    def decrypt_share(self, key, iv, ciphertext):
        block_size = 16
        ciphertext = base64.b64decode(ciphertext)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(block_size * 8).unpadder()
        data_without_padding = unpadder.update(
            plaintext) + unpadder.finalize()
        return data_without_padding.decode()
