"""Crib-driven searches over classical cipher families for K4.

Each search asks: is there *any* key for this cipher family that maps the K4
ciphertext onto the published cribs? A family that cannot even satisfy the
cribs is ruled out, independent of what the rest of the plaintext says.
"""

from itertools import permutations

import numpy as np

from .core import AZ, K4, KA, VARIANTS, crib_positions

ALPHABETS = {"AZ": AZ, "KA": KA}
CRIB = sorted(crib_positions().items())
CRIB_IDX = np.array([i for i, _ in CRIB])


def _key_values(alphabet, variant, ct_positions, ct_text=K4):
    """Key indices implied by the cribs, given which ct position holds each crib letter."""
    idx = {ch: i for i, ch in enumerate(alphabet)}
    ct = np.array([idx[c] for c in ct_text])
    pt = np.array([idx[p] for _, p in CRIB])
    c = ct[ct_positions]
    return VARIANTS[variant](c, pt)


def _periodic_ok(keys, residues):
    """Rows where equal residues always carry equal key values."""
    ok = np.ones(keys.shape[0], dtype=bool)
    n = keys.shape[1]
    for a in range(n):
        for b in range(a + 1, n):
            ok &= ~((residues[:, a] == residues[:, b]) & (keys[:, a] != keys[:, b]))
    return ok


def constraints(residues):
    """Number of crib letters that are checked rather than free (24 - distinct residues)."""
    return len(residues) - len(set(residues))


def periodic_substitution(max_period=48):
    """Direct periodic Vigenere / Beaufort / variant Beaufort, both alphabets."""
    hits = []
    for aname, alph in ALPHABETS.items():
        for var in VARIANTS:
            k = _key_values(alph, var, CRIB_IDX)[None, :]
            for p in range(1, max_period + 1):
                res = (CRIB_IDX % p)[None, :]
                if _periodic_ok(k, res)[0]:
                    hits.append((aname, var, p, constraints(res[0])))
    return hits


def autokey():
    """Plaintext- and ciphertext-autokey with primer length L (primer unknown)."""
    hits = []
    crib = dict(CRIB)
    for aname, alph in ALPHABETS.items():
        idx = {ch: i for i, ch in enumerate(alph)}
        for var, rel in VARIANTS.items():
            for L in range(1, 97):
                checked = ok = 0
                for i, p in crib.items():
                    k = rel(idx[K4[i]], idx[p])
                    if i - L < 0:
                        continue
                    # ciphertext autokey: key = earlier ciphertext letter
                    checked += 1
                    ok += k == idx[K4[i - L]]
                if checked and ok == checked:
                    hits.append((aname, var, "ct-autokey", L, checked))
                checked = ok = 0
                for i, p in crib.items():
                    if i - L in crib:
                        checked += 1
                        ok += rel(idx[K4[i]], idx[p]) == idx[crib[i - L]]
                if checked and ok == checked:
                    hits.append((aname, var, "pt-autokey", L, checked))
    return hits


def columnar_order(width, perm, n=97):
    """Ciphertext position of each plaintext index for keyed columnar transposition."""
    cols = [list(range(c, n, width)) for c in range(width)]
    order = [i for col in perm for i in cols[col]]
    pos = np.empty(n, dtype=int)
    pos[order] = np.arange(n)
    return pos


def columnar_plus_periodic(widths=range(2, 9), max_period=26, min_constraints=6, ct=K4):
    """Columnar transposition combined with periodic substitution, in either order.

    'sub_first':   C = T(Sub(P)) -> key index follows plaintext position.
    'trans_first': C = Sub(T(P)) -> key index follows ciphertext position.
    """
    hits = []
    for w in widths:
        perms = list(permutations(range(w)))
        pos = np.array([columnar_order(w, p)[CRIB_IDX] for p in perms])
        for aname, alph in ALPHABETS.items():
            for var in VARIANTS:
                keys = _key_values(alph, var, pos, ct)
                for p in range(1, max_period + 1):
                    for order, res in (
                        ("sub_first", np.broadcast_to(CRIB_IDX % p, pos.shape)),
                        ("trans_first", pos % p),
                    ):
                        ok = np.nonzero(_periodic_ok(keys, res))[0]
                        for r in ok:
                            c = constraints(res[r])
                            if c >= min_constraints:
                                hits.append((w, perms[r], aname, var, p, order, c))
    return hits


if __name__ == "__main__":
    print("periodic substitution:", periodic_substitution())
    print("autokey:", autokey())
