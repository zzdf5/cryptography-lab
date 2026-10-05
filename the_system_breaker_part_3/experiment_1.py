# Experiment 1: A key space smaller than it looks
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


def multiplicative_encrypt(plaintext: str, k: int) -> str:
    ciphertext = ""
    for letter in plaintext:
        P = ord(letter) - ord("A")
        C = (P * k) % 26
        ciphertext += chr(C + ord("A"))
    return ciphertext


def multiplicative_decrypt(ciphertext: str, k: int) -> str | None:
    inv = mod_inverse(k, 26)
    if inv is None:
        return None
    plaintext = ""
    for letter in ciphertext:
        C = ord(letter) - ord("A")
        P = (C * inv) % 26
        plaintext += chr(P + ord("A"))
    return plaintext


# sweep every key from 1 to 25

print("=== Multiplicative cipher keys (mod 26) ===")
print("+-----+-----------+---------+")
print("|  k  | gcd(k,26) | inverse |")
print("+-----+-----------+---------+")

for k in range(1, 26):
    g = gcd(k, 26)
    inv = mod_inverse(k, 26)
    inv_str = str(inv) if inv is not None else "none"
    print(f"| {k:>3} | {g:>9} | {inv_str:>7} |")

print("+-----+-----------+---------+")

valid_keys = [k for k in range(1, 26) if mod_inverse(k, 26) is not None]
print(f"\nValid keys: {len(valid_keys)} of 25")

# demonstrate with RAHASIA

print()
word = "RAHASIA"

for k in [2, 3, 5]:
    enc = multiplicative_encrypt(word, k)
    inv = mod_inverse(k, 26)
    dec = multiplicative_decrypt(enc, k)
    if dec is not None:
        print(
            f"k = {k} -> {word} becomes {enc}, decrypted back to {dec} (inverse {inv})")
    else:
        print(
            f"k = {k} -> {word} becomes {enc}, cannot be decrypted (no inverse)")
