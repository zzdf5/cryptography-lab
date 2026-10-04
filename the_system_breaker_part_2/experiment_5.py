# Experiment 5: Breaking the Vigenere cipher with the Kasiski method
# "The System Breaker" series, Part 2 - Joaquin Thiogo

from collections import Counter
from itertools import combinations
from math import gcd

# --- Vigenere Cipher ---


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Encrypt the plaintext with the Vigenere cipher."""
    result = ""
    key = key.upper()
    key_index = 0

    for ch in plaintext:
        if ch.isalpha():
            # Turn the key letter into a shift value from 0 to 25.
            shift = ord(key[key_index % len(key)]) - ord('A')

            # Use the matching ASCII base for uppercase or lowercase letters.
            base = ord('A') if ch.isupper() else ord('a')

            # Shift the plaintext letter by the current key letter.
            result += chr((ord(ch) - base + shift) % 26 + base)
            key_index += 1
        else:
            # Spaces and other characters are not encrypted.
            result += ch
    return result


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt the ciphertext with the Vigenere cipher."""
    result = ""
    key = key.upper()
    key_index = 0

    for ch in ciphertext:
        if ch.isalpha():
            # Calculate the shift from the current key letter.
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if ch.isupper() else ord('a')

            # Shift the letter back to get the plaintext.
            result += chr((ord(ch) - base - shift) % 26 + base)
            key_index += 1
        else:
            # Keep spaces and non-letter characters.
            result += ch
    return result


# --- Kasiski Examination ---


def kasiski_examination(ciphertext: str, seq_lens: tuple[int, ...] = (3, 4, 5), max_factor: int = 20, top_n: int = 8, max_gap: int = 800) -> list[int]:
    """Find candidate key lengths with the Kasiski examination."""

    # Remove non-letter characters so positions in the ciphertext are easier to analyze.
    clean_text = "".join(c for c in ciphertext.upper() if c.isalpha())

    # Longer patterns are less likely to repeat by chance, so they get more weight.
    weight = {seq_len: seq_len - 1 for seq_len in seq_lens}

    print("Steps 1 and 2: Find repeated patterns and measure their distances")
    weighted_gaps = []

    for seq_len in seq_lens:
        sequences = {}

        # Take every piece of the ciphertext with length seq_len.
        for i in range(len(clean_text) - seq_len + 1):
            seq = clean_text[i:i + seq_len]
            sequences.setdefault(seq, []).append(i)

        for seq, positions in sequences.items():
            if len(positions) > 1:
                # Measure the distance between every pair of occurrences of the same pattern.
                seq_gaps = [
                    b - a
                    for a, b in combinations(positions, 2)
                    if (b - a) <= max_gap
                ]

                if seq_gaps:
                    print(
                        f" - Pattern '{seq}' (len={seq_len}) at positions {positions} "
                        f"-> distances used = {seq_gaps}"
                    )

                # Store each distance with the weight of its pattern for the next step.
                for g in seq_gaps:
                    weighted_gaps.append((g, weight[seq_len]))

    if not weighted_gaps:
        print(" [!] No repetitions close enough to analyze.")
        return []

    print("\nStep 3: Analyze common factors and the GCD")

    # Collect all distances to find the GCD and candidate factors.
    gaps = [gap for gap, _ in weighted_gaps]

    # Find the GCD of all distances step by step.
    common_gcd = gaps[0]

    for gap in gaps[1:]:
        common_gcd = gcd(common_gcd, gap)

    print(f" - GCD of all distances: {common_gcd}")

    # Count how often each number from 2 to 20 divides a distance.
    factor_scores = Counter()

    for gap, w in weighted_gaps:
        for factor in range(2, max_factor + 1):
            if gap % factor == 0:
                factor_scores[factor] += w

    # If the GCD is within the candidate range, give it extra points.
    if 2 <= common_gcd <= max_factor:
        factor_scores[common_gcd] += 10
        print(
            f" - GCD {common_gcd} added as a candidate "
            f"with higher priority."
        )

    # Sort the candidates by score, highest first.
    ranked_factors = factor_scores.most_common(top_n)

    for factor, score in ranked_factors:
        print(f" - Possible key length {factor}: score {score}")

    return [factor for factor, _ in ranked_factors]


# --- Frequency Analysis ---

# Source: https://www.sttmedia.com/characterfrequency-indonesian
FREQUENCY_ID = {
    'A': 0.2039, 'B': 0.0264, 'C': 0.0076,
    'D': 0.0500, 'E': 0.0828, 'F': 0.0021,
    'G': 0.0366, 'H': 0.0274, 'I': 0.0798,
    'J': 0.0087, 'K': 0.0514, 'L': 0.0326,
    'M': 0.0421, 'N': 0.0933, 'O': 0.0126,
    'P': 0.0261, 'Q': 0.0001, 'R': 0.0464,
    'S': 0.0415, 'T': 0.0558, 'U': 0.0462,
    'V': 0.0018, 'W': 0.0048, 'X': 0.0003,
    'Y': 0.0188, 'Z': 0.0004
}


def find_key(ciphertext: str, key_length: int) -> tuple[str, float]:
    """Find the key for a given key length."""
    text = "".join(c.upper() for c in ciphertext if c.isalpha())
    key = ""
    total_score = 0.0

    for position in range(key_length):
        # Split the ciphertext into columns based on the key position.
        # Each column is basically a Caesar cipher.
        column = text[position::key_length]
        if len(column) < 5:
            return "", float("inf")
        best_shift = 0
        best_score = float("inf")

        for shift in range(26):
            # Try every possible shift for this column.
            counts = Counter(
                chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
                for c in column
            )
            total = len(column)
            score = 0.0

            # Compare the letter frequencies after shifting with Indonesian.
            for letter in FREQUENCY_ID:
                observed = counts.get(letter, 0)
                expected = FREQUENCY_ID[letter] * total
                if expected > 0:
                    score += (observed - expected) ** 2 / expected

            # Keep the shift whose letter distribution is closest to Indonesian.
            if score < best_score:
                best_score = score
                best_shift = shift

        # The best shift becomes one letter of the key.
        key += chr(best_shift + ord('A'))
        total_score += best_score

    return key, total_score


# --- Cracking Pipeline ---


def crack_vigenere(ciphertext: str, candidate_lengths: list[int]) -> tuple[str | None, int | None]:
    """Test each candidate key length and pick the one with the best score."""

    print("\nStep 4: Test each candidate key length")

    best_key = None
    best_length = None
    best_score = float("inf")

    for length in candidate_lengths:
        # Find the key for the length suggested by Kasiski.
        key, score = find_key(ciphertext, length)
        if not key:
            continue
        print(
            f" - Length {length} -> guessed key: '{key}', chi-squared score: {score:.2f}")

        # The lower the chi-squared score, the closer the text is to Indonesian.
        if score < best_score:
            best_score = score
            best_key = key
            best_length = length

    return best_key, best_length


# --- Experiment 5 ---

ciphertext = "Brpplwgiami slacao iduu paug emmgesabirz chrs ueeylmtcnpiraf xejau smxapa aivik uawal lisaja gtey pphss lriu ysvg kikac jeihhk emmsajafga. Ueugsv mvnngmvabau mwboue lnczigsp ysvg kewal uaba wekin iaoakqa uawal libiyiesae mllstuz jhravgrn fafo tzdhk suae slkstiguu tsvpr hhrma kyadalqr zspnqi abau dasekaoua wlvh vrsvg capn qinx tpdss mvmplasi buuca gaeg iefir."

candidates = kasiski_examination(ciphertext)
key, length = crack_vigenere(ciphertext, candidates)

print()
if key is None:
    print("The key length could not be found. The ciphertext may be too short.")
else:
    print(f"Best key length : {length}")
    print(f"Recovered key   : {key}")
    print(f"Plaintext       : {vigenere_decrypt(ciphertext, key)}")
