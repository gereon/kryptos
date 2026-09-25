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
| Keyed columnar transposition + periodic substitution, either order | A–Z, KRYPTOS | widths 2–9, periods 1–26, ≥6 checked crib letters | ruled out |

The planted-solution tests confirm the columnar search would find a real solution
of that form, so these are genuine eliminations rather than search bugs.
