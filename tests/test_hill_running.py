import random

import numpy as np

import kryptos.hill as hill
import kryptos.running_key as rk
from kryptos.core import AZ, CRIBS


def _plain():
    rng = random.Random(1)
    pt = [rng.choice(AZ) for _ in range(97)]
    for start, word in CRIBS.items():
        pt[start : start + len(word)] = word
    return pt


def test_hill_finds_planted_matrix(monkeypatch):
    M = np.array([[3, 2, 5], [1, 7, 4], [2, 9, 11]])
    pt = np.array([AZ.index(c) for c in _plain()])
    ct = "".join(AZ[v] for v in (pt[:96].reshape(-1, 3) @ M.T % 26).ravel()) + "A"
    monkeypatch.setattr(hill, "K4", ct)
    rows, _ = hill.solve(3, 0, AZ)
    for j in range(3):
        assert any((r == M[j]).all() for r in rows[j])


def test_running_key_finds_planted_offset(monkeypatch):
    rng = random.Random(2)
    source = "".join(rng.choice(AZ) for _ in range(5000))
    off = 1234
    pt = _plain()
    ct = "".join(AZ[(AZ.index(p) + AZ.index(source[off + i])) % 26] for i, p in enumerate(pt))
    top = rk.best_offsets(source, top=1, ct=ct)[0]
    assert top[0] == 24 and top[1:] == ("AZ", "vigenere", "fwd", off)
