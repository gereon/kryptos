"""Ciphertexts, cribs and basic cipher primitives for Kryptos."""

import string

AZ = string.ascii_uppercase
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"  # Kryptos-keyed alphabet used in K1/K2

K1 = "EMUFPHZLRFAXYUSDJKZLDKRNSHGNFIVJYQTQUXQBQVYUVLLTREVJYQTMKYRDMFD"
K4 = (
    "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
)

# Published plaintext cribs for K4 (0-indexed start positions).
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}


def crib_positions():
    """Map ciphertext position -> known plaintext letter."""
    return {start + i: ch for start, word in CRIBS.items() for i, ch in enumerate(word)}


# Key-letter relations: given ciphertext index c and plaintext index p in an alphabet,
# return the key index k.
VARIANTS = {
    "vigenere": lambda c, p: (c - p) % 26,  # C = P + K
    "beaufort": lambda c, p: (c + p) % 26,  # C = K - P
    "variant": lambda c, p: (p - c) % 26,  # C = P - K
}


def vigenere_decrypt(ct, key, alphabet=AZ):
    idx = {ch: i for i, ch in enumerate(alphabet)}
    return "".join(
        alphabet[(idx[c] - idx[key[i % len(key)]]) % 26] for i, c in enumerate(ct)
    )
