# Kryptos K4 search

Crib-driven elimination of classical cipher families for Kryptos K4, using the
published plaintext clues `EASTNORTHEAST` (positions 22–34) and `BERLINCLOCK` (64–74).

```
pip install numpy pytest
python -m pytest -q        # K1 sanity check + planted-solution tests
python -m kryptos.search   # direct periodic + autokey searches
```

## Results so far

| Family | Alphabets | Scope | Result |
|---|---|---|---|
| Vigenère / Beaufort / variant, periodic | A–Z, KRYPTOS | periods 1–48 | ruled out (periods 27–29 match only because they impose no constraint) |
| Plaintext / ciphertext autokey | A–Z, KRYPTOS | primer length 1–96 | ruled out |
| Keyed columnar transposition + periodic substitution, either order | A–Z, KRYPTOS | widths 2–10, periods 1–26, ≥6 checked crib letters | ruled out |
| Periodic substitution with *arbitrary* alphabets (covers all Quagmires, any keywords) | any | periods 1–48 | ruled out for periods 1–7, 9, 10, 14, 15, 17, 21, 25, 34, 42, 43, 45; other periods are unconstrained by the cribs |
| Same, after keyed columnar transposition (either order) | any | widths 2–8, periods 1–26 | no significant fit (best fits check only 4 crib letters; shuffled K4 gives as many) |
| Running key: K1–K3 plaintext, Carter's *Tomb of Tut.ankh.Amen* vols 1–2 | A–Z, KRYPTOS | every offset, forwards and reversed | ruled out (best 8/24, chance level) |
| Hill cipher | A–Z, KRYPTOS | 2×2, 3×3 all block phases; 4×4 phases 1–2 | ruled out |
| Any transposition-only or monoalphabetic(+transposition) cipher | — | — | ruled out: K4's index of coincidence is 0.036 (English ≈ 0.066) |

## Status of K4 (September 2026)

The plaintext was found in Sanborn's Smithsonian archive in 2025 but has not been
published. Paradigm holds it and verifies submissions against a keyed SHA-256 tag
($1 per guess), so a candidate cannot be verified offline. The encryption method
remains unpublished.

The planted-solution tests confirm the columnar search would find a real solution
of that form, so these are genuine eliminations rather than search bugs.
