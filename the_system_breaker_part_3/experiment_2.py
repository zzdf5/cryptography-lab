# Experiment 2: Building Rivest-Shamir-Adleman (RSA)
# "The System Breaker" series, Part 3 - Joaquin Thiogo

from math import gcd


def mod_inverse(a: int, n: int) -> int | None:
    # extended Euclidean Algorithm
    old_r, r = a, n
    old_s, s = 1, 0
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    if old_r != 1:
        return None
    return old_s % n


# step 1: choose two prime numbers
p = 101
q = 103

# step 2: compute n and phi(n)
n = p * q
phi = (p - 1) * (q - 1)

# step 3: choose public exponent e where gcd(e, phi) = 1
e = 2
while gcd(e, phi) != 1:
    e += 1

# step 4: find private exponent d as the modular inverse of e
d = mod_inverse(e, phi)

# step 5: encrypt and decrypt the message
m = 9  # the letter J
c = pow(m, e, n)
decipher = pow(c, d, n)

print("=== Key generation ===")
print(f"p = {p}, q = {q}")
print(f"n   = {n}")
print(f"phi = {phi}")
print(f"public key  (e, n) = ({e}, {n})")
print(f"private key (d, n) = ({d}, {n})")

print("\n=== Encryption and decryption ===")
print(f"m = {m}")
print(f"c = {m}^{e} mod {n} = {c}")
print(f"m = {c}^{d} mod {n} = {decipher}")
