# Experiment 2: Breaking the Caesar cipher with brains
# "The System Breaker" series, Part 2 - Joaquin Thiogo

from collections import Counter

plaintext = "Kami putra dan putri Indonesia mengaku bertumpah darah yang satu, tanah Indonesia. Kami putra dan putri Indonesia mengaku berbangsa yang satu, bangsa Indonesia. Kami putra dan putri Indonesia menjunjung bahasa persatuan, bahasa Indonesia."


def caesar_encrypt(plaintext: str, k: int) -> str:
    ciphertext = ""
    for letter in plaintext.upper():
        if letter.isalpha():
            P = ord(letter) - ord("A")
            C = (P + k) % 26
            ciphertext += chr(C + ord("A"))
        else:
            ciphertext += letter
    return ciphertext


def caesar_decrypt(ciphertext: str, k: int) -> str:
    plaintext = ""
    for letter in ciphertext.upper():
        if letter.isalpha():
            C = ord(letter) - ord("A")
            P = (C - k) % 26
            plaintext += chr(P + ord("A"))
        else:
            plaintext += letter
    return plaintext


def guess_key(ciphertext: str) -> int:
    # count how often each letter appears
    counts: dict[str, int] = {}
    for letter in ciphertext:
        if letter.isalpha():
            counts[letter] = counts.get(letter, 0) + 1

    # assume the most frequent letter is the encryption of 'A'
    top_letter = max(counts, key=lambda letter: counts[letter])

    C = ord(top_letter) - ord("A")
    P = 0
    return (C - P) % 26


# secret key
k = 7
ciphertext = caesar_encrypt(plaintext, k)

# count the frequency of each letter
letters = [letter for letter in ciphertext if letter.isalpha()]
counts = Counter(letters)
total = len(letters)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# sort in descending order, if they are the same, sort alphabetically
ranking = sorted(alphabet, key=lambda letter: (-counts[letter], letter))

print(f"Letters in ciphertext: {total}")
print()
print("=== Letter frequencies in the ciphertext ===")
print("+--------+-------+---------+")
print("| letter | count | percent |")
print("+--------+-------+---------+")
for letter in ranking:
    print(
        f"| {letter:^6} | {counts[letter]:>5} | {counts[letter] / total:>7.1%} |")
print("+--------+-------+---------+")
print()

# guess key and then decrypt the ciphertext
guessed_k = guess_key(ciphertext)
top_letter = ranking[0]
print(f"Assume '{top_letter}' is the encryption of 'A'")
print(f"Key = {top_letter} - A = {ord(top_letter) - ord('A')} - 0 = {guessed_k}")
print()
print("=== Decrypted with the guessed key ===")
print(caesar_decrypt(ciphertext, guessed_k))
