# Exposing the pair leak in the Playfair cipher
# "The System Breaker" series, Part 2 - Joaquin Thiogo

from collections import Counter

plaintext = "Kami putra dan putri Indonesia mengaku bertumpah darah yang satu, tanah Indonesia. Kami putra dan putri Indonesia mengaku berbangsa yang satu, bangsa Indonesia. Kami putra dan putri Indonesia menjunjung bahasa persatuan, bahasa Indonesia."


def only_letters(text: str) -> str:
    return "".join(letter for letter in text.upper() if letter.isalpha())


def build_grid(keyword: str) -> str:
    # 5x5 grid as one string
    grid = ""
    for letter in only_letters(keyword) + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        letter = "I" if letter == "J" else letter
        if letter not in grid:
            grid += letter
    return grid


def make_pairs(plaintext: str) -> list[str]:
    # split into pairs and insert 'X' between double letters
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
    return pairs


def encrypt_pair(pair: str, grid: str) -> str:
    row1, col1 = divmod(grid.index(pair[0]), 5)
    row2, col2 = divmod(grid.index(pair[1]), 5)
    if row1 == row2:
        return grid[row1 * 5 + (col1 + 1) % 5] + grid[row2 * 5 + (col2 + 1) % 5]
    if col1 == col2:
        return grid[(row1 + 1) % 5 * 5 + col1] + grid[(row2 + 1) % 5 * 5 + col2]
    return grid[row1 * 5 + col2] + grid[row2 * 5 + col1]


# secret key
grid = build_grid("MONARCHY")
plain_pairs = make_pairs(plaintext)
cipher_pairs = [encrypt_pair(pair, grid) for pair in plain_pairs]

# The attacker only sees the ciphertext pairs. The last column is only used to check the guess.
cipher_counts = Counter(cipher_pairs)
print(f"Pairs in ciphertext: {len(cipher_pairs)}")
print()
print("=== Five most common ciphertext pairs ===")
print("+-----------------+-------+---------------------+")
print("| ciphertext pair | count | real plaintext pair |")
print("+-----------------+-------+---------------------+")
for pair, count in cipher_counts.most_common(5):
    original = plain_pairs[cipher_pairs.index(pair)]
    print(f"| {pair:^15} | {count:>5} | {original:^19} |")
print("+-----------------+-------+---------------------+")
print()
print("=== Mirrored pairs ===")
for pair in ["AN", "NG", "KA"]:
    mirrored = pair[::-1]
    print(f"{pair} -> {encrypt_pair(pair, grid)}    {mirrored} -> {encrypt_pair(mirrored, grid)}")
