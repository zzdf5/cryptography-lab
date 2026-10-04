# Experiment 4: Comparing all five ciphers with the Index of Coincidence
# "The System Breaker" series, Part 2 - Joaquin Thiogo

plaintext = "Kami putra dan putri Indonesia mengaku bertumpah darah yang satu, tanah Indonesia. Kami putra dan putri Indonesia mengaku berbangsa yang satu, bangsa Indonesia. Kami putra dan putri Indonesia menjunjung bahasa persatuan, bahasa Indonesia."


def only_letters(text: str) -> str:
    return "".join(letter for letter in text.upper() if letter.isalpha())


def caesar_encrypt(plaintext: str, k: int) -> str:
    ciphertext = ""
    for letter in only_letters(plaintext):
        P = ord(letter) - ord("A")
        C = (P + k) % 26
        ciphertext += chr(C + ord("A"))
    return ciphertext


def affine_encrypt(plaintext: str, a: int, b: int) -> str:
    ciphertext = ""
    for letter in only_letters(plaintext):
        P = ord(letter) - ord("A")
        C = (a * P + b) % 26
        ciphertext += chr(C + ord("A"))
    return ciphertext


def hill_encrypt(plaintext: str, K: list[list[int]]) -> str:
    letters = only_letters(plaintext)
    if len(letters) % 2 == 1:
        letters += "X"
    ciphertext = ""
    for i in range(0, len(letters), 2):
        P1 = ord(letters[i]) - ord("A")
        P2 = ord(letters[i + 1]) - ord("A")
        C1 = (K[0][0] * P1 + K[0][1] * P2) % 26
        C2 = (K[1][0] * P1 + K[1][1] * P2) % 26
        ciphertext += chr(C1 + ord("A")) + chr(C2 + ord("A"))
    return ciphertext


def playfair_encrypt(plaintext: str, keyword: str) -> str:
    grid = ""
    for letter in only_letters(keyword) + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        letter = "I" if letter == "J" else letter
        if letter not in grid:
            grid += letter

    letters = only_letters(plaintext).replace("J", "I")
    pairs: list[str] = []
    i = 0
    while i < len(letters):
        first = letters[i]
        second = letters[i + 1] if i + 1 < len(letters) else "X"
        if first == second:
            pairs.append(first + "X")
            i += 1
        else:
            pairs.append(first + second)
            i += 2

    ciphertext = ""
    for pair in pairs:
        row1, col1 = divmod(grid.index(pair[0]), 5)
        row2, col2 = divmod(grid.index(pair[1]), 5)
        if row1 == row2:
            ciphertext += grid[row1 * 5 +
                               (col1 + 1) % 5] + grid[row2 * 5 + (col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += grid[(row1 + 1) % 5 * 5 + col1] + \
                grid[(row2 + 1) % 5 * 5 + col2]
        else:
            ciphertext += grid[row1 * 5 + col2] + grid[row2 * 5 + col1]
    return ciphertext


def vigenere_encrypt(plaintext: str, keyword: str) -> str:
    letters = only_letters(plaintext)
    ciphertext = ""
    for i, letter in enumerate(letters):
        P = ord(letter) - ord("A")
        k = ord(keyword[i % len(keyword)]) - ord("A")
        C = (P + k) % 26
        ciphertext += chr(C + ord("A"))
    return ciphertext


def index_of_coincidence(text: str) -> float:
    # probability that two randomly picked letters in the text are the same
    letters = only_letters(text)
    N = len(letters)
    total = 0
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        f = letters.count(letter)
        total += f * (f - 1)
    return total / (N * (N - 1))


results = [
    ("Plaintext (no encryption)", plaintext),
    ("Caesar, k = 7", caesar_encrypt(plaintext, 7)),
    ("Affine, a = 5, b = 8", affine_encrypt(plaintext, 5, 8)),
    ("Playfair, MONARCHY", playfair_encrypt(plaintext, "MONARCHY")),
    ("Hill, [[3, 3], [2, 5]]", hill_encrypt(plaintext, [[3, 3], [2, 5]])),
    ("Vigenere, KUNCI", vigenere_encrypt(plaintext, "KUNCI")),
]

print("+---------------------------+--------+")
print("| text                      |   IC   |")
print("+---------------------------+--------+")
for name, text in results:
    print(f"| {name:<25} | {index_of_coincidence(text):.4f} |")
print("+---------------------------+--------+")
print(f"| {'Random text (1/26)':<25} | {1 / 26:.4f} |")
print("+---------------------------+--------+")
