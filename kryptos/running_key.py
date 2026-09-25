"""Running-key search: key stream taken from a source text at some offset.

With 24 crib letters, a random text/offset matches all of them with probability
26**-24, so a full match is conclusive; partial matches are reported for triage
(random expectation is about 24/26 matched letters).
"""

import re

import numpy as np

from .core import K4, VARIANTS
from .search import ALPHABETS, CRIB, CRIB_IDX, _key_values


def letters(text):
    return re.sub(r"[^A-Z]", "", text.upper())


def best_offsets(source, top=3, ct=None):
    """Best (matches, alphabet, variant, direction, offset) over all key alignments."""
    results = []
    for aname, alph in ALPHABETS.items():
        idx = {ch: i for i, ch in enumerate(alph)}
        for direction, src in (("fwd", source), ("rev", source[::-1])):
            s = np.array([idx[c] for c in src])
            if len(s) < len(K4):
                continue
            n = len(s) - len(K4) + 1
            window = s[np.arange(n)[:, None] + CRIB_IDX[None, :]]  # n x 24
            for var in VARIANTS:
                need = _key_values(alph, var, CRIB_IDX, ct)
                score = (window == need[None, :]).sum(axis=1)
                for o in np.argsort(-score)[:top]:
                    results.append((int(score[o]), aname, var, direction, int(o)))
    return sorted(results, reverse=True)[:top]
