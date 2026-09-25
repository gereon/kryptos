"""Hill cipher (n x n matrix mod 26) against the K4 cribs.

Each ciphertext coordinate depends on one matrix row only, so each row is
brute-forced independently over all crib blocks that lie fully inside a crib.
"""

from itertools import product

import numpy as np

from .core import K4, crib_positions
from .search import ALPHABETS


def crib_blocks(n, phase):
    known = crib_positions()
    blocks = []
    for start in range(phase, 97 - n + 1, n):
        span = range(start, start + n)
        if all(i in known for i in span):
            blocks.append(span)
    return known, blocks


def solve(n, phase, alphabet):
    idx = {c: i for i, c in enumerate(alphabet)}
    known, blocks = crib_blocks(n, phase)
    if len(blocks) <= n:
        return None, len(blocks)
    P = np.array([[idx[known[i]] for i in b] for b in blocks])  # blocks x n
    C = np.array([[idx[K4[i]] for i in b] for b in blocks])
    rows = np.array(list(product(range(26), repeat=n)))  # 26^n x n
    PR = rows @ P.T % 26  # candidates x blocks
    per_coord = [rows[(PR == C[:, j][None, :]).all(axis=1)] for j in range(n)]
    return per_coord, len(blocks)


if __name__ == "__main__":
    for n in (2, 3, 4):
        for phase in range(n):
            for aname, alph in ALPHABETS.items():
                sol, nb = solve(n, phase, alph)
                counts = None if sol is None else [len(r) for r in sol]
                print(f"n={n} phase={phase} {aname}: {nb} crib blocks, rows fitting per coord={counts}")
