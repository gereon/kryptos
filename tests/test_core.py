from kryptos.core import K1, K4, KA, crib_positions, vigenere_decrypt


def test_k1_decrypts_with_palimpsest():
    pt = vigenere_decrypt(K1, "PALIMPSEST", KA)
    assert pt.startswith("BETWEENSUBTLESHADING")


def test_k4_shape():
    assert len(K4) == 97
    assert len(crib_positions()) == 24
