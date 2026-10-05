# Experiment 3: Breaking RSA two ways
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


# known to the attacker
n = 10403
e = 7
c = 7992

print(f"Known to the attacker: n = {n}, e = {e}, c = {c}")

# attack 1: factor n

p = 2
factor_attempts = 0
while p * p <= n:
    factor_attempts += 1
    if n % p == 0:
        q = n // p
        break
    p += 1

phi = (p - 1) * (q - 1)
d = mod_inverse(e, phi)
message_1 = pow(c, d, n)

print(f"\n=== Attack 1: factor n ===")
print(f"found p = {p}, q = {q} after {factor_attempts} attempts")
print(f"recovered d = {d}")
print(f"decrypted message = {message_1}")

# attack 2: guess the message

m_guess = 0
guess_attempts = 0
while m_guess < 26:
    guess_attempts += 1
    if pow(m_guess, e, n) == c:
        break
    m_guess += 1

print(f"\n=== Attack 2: guess the message ===")
print(f"found message = {m_guess} after {guess_attempts} attempts")
