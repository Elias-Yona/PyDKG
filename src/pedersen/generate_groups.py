import secrets


class CyclicGroup:
    def __init__(self, bit_length):
        self.bit_length = bit_length
        self.p, self.g, self.h = self.__generate_cyclic_group()

    def __is_prime(self, num):
        """Check if a number is prime"""
        if num < 2:
            return False
        for i in range(2, int(num**0.5)+1):
            if num % i == 0:
                return False
        return True

    def __get_primes(self):
        """Generate a list of primes within a specified bit length"""
        primes = []
        lower = 2**(self.bit_length-1)
        upper = 2**self.bit_length
        for num in range(lower, upper):
            if self.__is_prime(num):
                primes.append(num)
        return primes

    def __get_generator(self, p):
        """Find a generator of a cyclic group of prime order"""
        factors = []
        phi = p-1
        n = phi
        for i in range(2, int(p**0.5)+1):
            if n % i == 0:
                factors.append(i)
                while n % i == 0:
                    n //= i
        if n > 1:
            factors.append(n)
        for g in range(2, p):
            flag = True
            for factor in factors:
                if pow(g, phi//factor, p) == 1:
                    flag = False
                    break
            if flag:
                return g

    def __generate_cyclic_group(self):
        """Generate a cyclic group of prime order"""
        primes = self.__get_primes()
        while not primes:
            self.bit_length += 1
            primes = self.__get_primes()
        p = secrets.choice(primes)
        g = self.__get_generator(p)
        h = self.__get_generator(p)
        return p, g, h


# Example usage
# group = CyclicGroup(20)
# print("p:", group.p)
# print("g:", group.g)
# print("h:", group.h)
