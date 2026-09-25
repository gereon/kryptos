"""Periodic substitution with an *arbitrary* alphabet per key position.

Covers Vigenere, Beaufort, all Quagmires and any keyed/mixed alphabets. The only
constraint is that, within one residue class, the ct<->pt map is a bijection.
"""

from .core import K4, crib_positions


def consistent(pairs):
    fwd, back = {}, {}
    for c, p in pairs:
        if fwd.setdefault(c, p) != p or back.setdefault(p, c) != c:
            return False
    return True


def checked_pairs(groups):
    """Crib letters beyond the first occurrence of each ct letter / pt letter per class."""
    return sum(len(g) - len({c for c, _ in g}) + len(g) - len({p for _, p in g}) for g in groups.values())


def periodic_general(max_period=48, ct=None, pos_map=None, key_pos="pt"):
    """Periods at which some per-residue bijection fits the cribs.

    pos_map maps plaintext index -> ciphertext index (identity if None).
    key_pos: whether the key cycles with the plaintext ('pt') or ciphertext ('ct') index.
    """
    ct = ct or K4
    ok = []
    for p in range(1, max_period + 1):
        groups = {}
        for i, pt in crib_positions().items():
            j = pos_map[i] if pos_map is not None else i
            r = (i if key_pos == "pt" else j) % p
            groups.setdefault(r, []).append((ct[j], pt))
        if all(consistent(g) for g in groups.values()):
            ok.append((p, checked_pairs(groups)))
    return ok


if __name__ == "__main__":
    print(periodic_general())
