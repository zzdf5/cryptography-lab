# Experiment 1: Breaking the Caesar cipher with muscle
# "The System Breaker" series, Part 2 - Joaquin Thiogo

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


# secret key
k = 7
ciphertext = caesar_encrypt(plaintext, k)

print("=== Intercepted ciphertext ===")
print(ciphertext)
print()

# brute forcing all 26 keys
print("=== Trying all 26 keys ===")
for k in range(26):
    print(f"{k:>3} | {caesar_decrypt(ciphertext, k)[:30]}")
