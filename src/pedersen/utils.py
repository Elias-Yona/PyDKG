import sympy


def get_modulus(t):
    # Search for the first prime number greater than t
    q = t + 1
    while not sympy.isprime(q):
        q += 1

    # Check if q is a safe prime
    p = (q - 1) // 2
    if sympy.isprime(p):
        return q
    else:
        # If q is not a safe prime, search for the next prime number
        return get_modulus(q)


print(get_modulus(2))
