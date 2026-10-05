# Experiment 4: Counting the cost of an attack
# "The System Breaker" series, Part 3 - Joaquin Thiogo

def search_space(C: int, L: int) -> int:
    return C ** L


def fmt_space(C: int, L: int) -> str:
    N = search_space(C, L)
    if N < 1000:
        return str(N)
    exp = len(str(int(N))) - 1
    base = N / (10 ** exp)
    return f"{base:.1f} x 10^{exp}"


def time_to_exhaust(C: int, L: int, R: float) -> str:
    N = search_space(C, L)
    seconds = N / R
    years = seconds / (365.25 * 24 * 3600)
    if years < 1 / (365.25 * 24):
        return "instant"
    if years < 1:
        return f"~{years * 365.25:.0f} days"
    exp = len(str(int(years))) - 1
    return f"~10^{exp} years"


R = 1e18

systems = [
    ("Caesar",                  26,   1),
    ("Multiplicative cipher",   12,   1),
    ("Vigenere, 7-letter key",  26,   7),
    ("RSA n = 10403, factor n", 101,  1),
    ("AES-128",                 2,  128),
]

COL1 = 25
COL2 = 14
COL3 = 17

sep = f"+{'-'*COL1}+{'-'*COL2}+{'-'*COL3}+"
header = f"| {'system':<{COL1-2}} | {'search space':<{COL2-2}} | {'time to exhaust':<{COL3-2}} |"

print(sep)
print(header)
print(sep)

for name, C, L in systems:
    space = fmt_space(C, L)
    t = time_to_exhaust(C, L, R)
    print(f"| {name:<{COL1-2}} | {space:<{COL2-2}} | {t:<{COL3-2}} |")

print(sep)
print(f"\nAge of the universe: ~1.4 x 10^10 years")

aes_years = search_space(2, 128) / R / (365.25 * 24 * 3600)
print(
    f"AES-128 sweep: ~{aes_years:.2e} years (~{aes_years/1.4e10:.0f}x age of universe)")
