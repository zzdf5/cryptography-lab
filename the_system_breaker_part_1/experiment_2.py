# Experiment 2: Hashing passwords with SHA-256
# "The System Breaker" series, Part 1 - Joaquin Thiogo

import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_login(username: str, password: str, database: dict) -> bool:
    return hash_password(password) == database.get(username)


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


users = {
    "alice": "user123",
    "bob": "password",
    "charlie": "abc123!",
    "dave": "password"
}

# registration: only the hash is stored
database = {}
for user, pw in users.items():
    database[user] = hash_password(pw)

print("=== Stored in the database ===")
rows = []
for user, stored in database.items():
    rows.append([user, stored])
print_table(["username", "password_hash"], rows)

# login: the typed password is hashed and compared
print("\n=== Login attempts ===")
attempts = [("bob", "password"), ("bob", "Password")]
rows = []
for user, typed in attempts:
    result = "success" if verify_login(user, typed, database) else "failed"
    rows.append([user, typed, result])
print_table(["username", "typed", "result"], rows)
