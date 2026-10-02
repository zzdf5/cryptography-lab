import base64


def encode_password(password: str) -> str:
    return base64.b64encode(password.encode("utf-8")).decode("ascii")


def decode_password(encoded: str) -> str:
    return base64.b64decode(encoded).decode("utf-8")


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
    "charlie": "abc123!"
}

database = {}
for user, pw in users.items():
    database[user] = encode_password(pw)

print("=== Stored in the database ===")
rows = []
for user, stored in database.items():
    rows.append([user, stored])
print_table(["username", "password"], rows)

print("\n=== Decoded by an attacker ===")
rows = []
for user, stored in database.items():
    rows.append([user, stored, decode_password(stored)])
print_table(["username", "password", "decoded"], rows)
