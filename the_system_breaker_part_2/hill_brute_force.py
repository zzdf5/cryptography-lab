# Breaking the Hill cipher by trying every valid key
# "The System Breaker" series, Part 2 - Joaquin Thiogo

from math import gcd

plaintext = "Kami putra dan putri Indonesia mengaku bertumpah darah yang satu, tanah Indonesia. Kami putra dan putri Indonesia mengaku berbangsa yang satu, bangsa Indonesia. Kami putra dan putri Indonesia menjunjung bahasa persatuan, bahasa Indonesia."

# Indonesian letter frequencies (source: sttmedia.com/characterfrequency-indonesian)
INDONESIAN_FREQUENCY = [
    0.2039, 0.0264, 0.0076, 0.0500, 0.0828, 0.0021, 0.0366, 0.0274, 0.0798,
    0.0087, 0.0514, 0.0326, 0.0421, 0.0933, 0.0126, 0.0261, 0.0001, 0.0464,
    0.0415, 0.0558, 0.0462, 0.0018, 0.0048, 0.0003, 0.0188, 0.0004,
]


def only_letters(text: str) -> str:
    return "".join(letter for letter in text.upper() if letter.isalpha())


def hill_apply(text: str, K: list[list[int]]) -> str:
    # multiply each letter pair by the 2x2 matrix K (used for both encrypt and decrypt)
    letters = only_letters(text)
    if len(letters) % 2 == 1:
        letters += "X"
    result = ""
    for i in range(0, len(letters), 2):
        P1 = ord(letters[i]) - ord("A")
        P2 = ord(letters[i + 1]) - ord("A")
        C1 = (K[0][0] * P1 + K[0][1] * P2) % 26
        C2 = (K[1][0] * P1 + K[1][1] * P2) % 26
        result += chr(C1 + ord("A")) + chr(C2 + ord("A"))
    return result


def inverse_2x2(M: list[list[int]]) -> list[list[int]]:
    det = (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % 26
    det_inverse = pow(det, -1, 26)
    return [
        [(M[1][1] * det_inverse) % 26, (-M[0][1] * det_inverse) % 26],
        [(-M[1][0] * det_inverse) % 26, (M[0][0] * det_inverse) % 26],
    ]


def chi_squared(text: str) -> float:
    # lower score = letter frequencies closer to Indonesian.
    counts = [0] * 26
    for letter in text:
        counts[ord(letter) - ord("A")] += 1
    total = len(text)
    score = 0.0
    for i in range(26):
        expected = INDONESIAN_FREQUENCY[i] * total
        score += (counts[i] - expected) ** 2 / expected
    return score


# secret key
secret_K = [[3, 3], [2, 5]]
ciphertext = hill_apply(plaintext, secret_K)

# try every 2x2 matrix D as the decryption matrix
# skip matrices whose determinant shares a factor with 26, since they have no inverse.
results: list[tuple[float, list[list[int]], str]] = []
tried = 0
for p in range(26):
    for q in range(26):
        for r in range(26):
            for s in range(26):
                if gcd((p * s - q * r) % 26, 26) != 1:
                    continue
                tried += 1
                D = [[p, q], [r, s]]
                candidate = hill_apply(ciphertext, D)
                results.append((chi_squared(candidate), D, candidate))

results.sort(key=lambda result: result[0])

print(f"Tried {tried} valid keys. Three best candidates:")
print("+------+---------------------+-------------+--------------------------------+")
print("| rank | key K               | chi-squared | decrypted (preview)            |")
print("+------+---------------------+-------------+--------------------------------+")
for rank, (score, D, text) in enumerate(results[:3], start=1):
    K = inverse_2x2(D)
    print(f"| {rank:^4} | {str(K):<19} | {score:>11.1f} | {text[:30]:<30} |")
print("+------+---------------------+-------------+--------------------------------+")
