# Experiment 3: Trying all 312 Affine keys
# "The System Breaker" series, Part 2 - Joaquin Thiogo

from math import gcd

plaintext = "Kami putra dan putri Indonesia mengaku bertumpah darah yang satu, tanah Indonesia. Kami putra dan putri Indonesia mengaku berbangsa yang satu, bangsa Indonesia. Kami putra dan putri Indonesia menjunjung bahasa persatuan, bahasa Indonesia."

# Indonesian letter frequencies (source: sttmedia.com/characterfrequency-indonesian)
INDONESIAN_FREQUENCY = {
    "A": 0.2039, "B": 0.0264, "C": 0.0076, "D": 0.0500, "E": 0.0828,
    "F": 0.0021, "G": 0.0366, "H": 0.0274, "I": 0.0798, "J": 0.0087,
    "K": 0.0514, "L": 0.0326, "M": 0.0421, "N": 0.0933, "O": 0.0126,
    "P": 0.0261, "Q": 0.0001, "R": 0.0464, "S": 0.0415, "T": 0.0558,
    "U": 0.0462, "V": 0.0018, "W": 0.0048, "X": 0.0003, "Y": 0.0188,
    "Z": 0.0004,
}


def affine_encrypt(plaintext: str, a: int, b: int) -> str:
    ciphertext = ""
    for letter in plaintext.upper():
        if letter.isalpha():
            P = ord(letter) - ord("A")
            C = (a * P + b) % 26
            ciphertext += chr(C + ord("A"))
        else:
            ciphertext += letter
    return ciphertext


def affine_decrypt(ciphertext: str, a: int, b: int) -> str:
    a_inverse = pow(a, -1, 26)
    plaintext = ""
    for letter in ciphertext.upper():
        if letter.isalpha():
            C = ord(letter) - ord("A")
            P = (a_inverse * (C - b)) % 26
            plaintext += chr(P + ord("A"))
        else:
            plaintext += letter
    return plaintext


def chi_squared(text: str) -> float:
    # lower score = letter frequencies closer to Indonesian.
    letters = [letter for letter in text if letter.isalpha()]
    total = len(letters)
    score = 0.0
    for letter, frequency in INDONESIAN_FREQUENCY.items():
        observed = letters.count(letter)
        expected = frequency * total
        score += (observed - expected) ** 2 / expected
    return score


# only values of a that share no common factor with 26 can be used
valid_a = [a for a in range(1, 26) if gcd(a, 26) == 1]

# secret key
a, b = 5, 8
ciphertext = affine_encrypt(plaintext, a, b)

print("=== Intercepted ciphertext ===")
print(ciphertext)
print()

# try every possible key and score each result
results: list[tuple[float, int, int, str]] = []
for a in valid_a:
    for b in range(26):
        candidate = affine_decrypt(ciphertext, a, b)
        results.append((chi_squared(candidate), a, b, candidate))
results.sort()

print(f"Tried {len(results)} keys. Three best candidates:")
print("+------+-----+-----+-------------+--------------------------------+")
print("| rank |  a  |  b  | chi-squared | decrypted (preview)            |")
print("+------+-----+-----+-------------+--------------------------------+")
for rank, (score, a, b, text) in enumerate(results[:3], start=1):
    print(
        f"| {rank:^4} | {a:^3} | {b:^3} | {score:>11.1f} | {text[:30]:<30} |")
print("+------+-----+-----+-------------+--------------------------------+")
