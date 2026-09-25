import random

from kryptos.core import AZ, CRIBS, KA
from kryptos.search import autokey, columnar_order, columnar_plus_periodic, periodic_substitution


def _plant(width, perm, key, alphabet, sub_first):
    rng = random.Random(0)
    pt = [rng.choice(AZ) for _ in range(97)]
    for start, word in CRIBS.items():
        pt[start : start + len(word)] = word
    idx = {c: i for i, c in enumerate(alphabet)}
    pos = columnar_order(width, perm)
    sub = lambda ch, i: alphabet[(idx[ch] + idx[key[i % len(key)]]) % 26]
    ct = [""] * 97
    if sub_first:
        for i, ch in enumerate(pt):
            ct[pos[i]] = sub(ch, i)
    else:
        for i, ch in enumerate(pt):
            ct[pos[i]] = ch
        ct = [sub(ch, i) for i, ch in enumerate(ct)]
    return "".join(ct)


def test_finds_planted_columnar_vigenere():
    perm = (3, 0, 5, 1, 6, 2, 4)
    for sub_first, order in ((True, "sub_first"), (False, "trans_first")):
        ct = _plant(7, perm, "LAYER", KA, sub_first)
        hits = columnar_plus_periodic(widths=[7], max_period=5, ct=ct)
        assert (7, perm, "KA", "vigenere", 5, order) in [h[:6] for h in hits]


def test_k4_rules_out_direct_periodic_and_autokey():
    assert all(c == 0 for *_, c in periodic_substitution())
    assert autokey() == []
