# Experiment 3: Cracking SHA-256 hashes with a dictionary attack
# "The System Breaker" series, Part 1 - Joaquin Thiogo

import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def print_table(headers: list, rows: list) -> None:
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    line = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    print(line)
    print("| " + " | ".join(h.ljust(w)
          for h, w in zip(headers, widths)) + " |")
    print(line)
    for row in rows:
        print("| " + " | ".join(c.ljust(w)
              for c, w in zip(row, widths)) + " |")
    print(line)


# The leaked database from Experiment 2
leaked_database = {
    "alice": "e606e38b0d8c19b24cf0ee3808183162ea7cd63ff7912dbb22b5e803286b4446",
    "bob": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
    "charlie": "033b83d92431548e13424903c235a9922af56dd34d53c9b72b37cf158489213e",
    "dave": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
}

# A small list of commonly used passwords
wordlist = ["123456", "qwerty", "password", "admin", "user123", "abc123!"]

print(f"Loaded {len(leaked_database)} password hashes (SHA-256)")
print(f"Trying {len(wordlist)} candidate passwords...\n")

rows = []
for attempt, guess in enumerate(wordlist, start=1):
    guess_hash = hash_password(guess)
    for user, stored_hash in leaked_database.items():
        if guess_hash == stored_hash:
            rows.append([str(attempt), guess, user])
            print(f"{guess:<16} ({user})")

print(f"\n{len(rows)}/{len(leaked_database)} cracked in {len(wordlist)} guesses\n")

print("=== Cracked by guessing ===")
print_table(["guess #", "password", "username"], rows)
