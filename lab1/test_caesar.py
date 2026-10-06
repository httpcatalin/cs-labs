import unittest

from caesar import ALPHABET, N, decrypt, encrypt, permuted_alphabet, prepare_text

ENGLISH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class CaesarTest(unittest.TestCase):
    def test_romanian_alphabet(self):
        self.assertEqual(N, 31)
        self.assertEqual(ALPHABET.index("Ă"), 1)
        self.assertEqual(ALPHABET.index("Ș"), 22)
        self.assertEqual(ALPHABET.index("Ț"), 24)
        self.assertEqual(ALPHABET.index("Z"), 30)

    def test_handout_examples(self):
        self.assertEqual(encrypt("CIFRULCEZAR", 3, ENGLISH), "FLIUXOFHCDU")
        self.assertEqual(encrypt("BRUTEFORCEATTACK", 17, ENGLISH), "SILKVWFITVRKKRTB")
        self.assertEqual(decrypt("SILKVWFITVRKKRTB", 17, ENGLISH), "BRUTEFORCEATTACK")

    def test_handout_permutation_example(self):
        alphabet = permuted_alphabet("CRYPTOGRAPHY", ENGLISH)
        self.assertEqual(alphabet, "CRYPTOGAHBDEFIJKLMNQSUVWXZ")
        self.assertEqual(encrypt("CIFRULCEZAR", 3, alphabet), "PLKTXQPJYDT")

    def test_prepare_text(self):
        self.assertEqual(prepare_text("știință și artă"), "ȘTIINȚĂȘIARTĂ")
        self.assertEqual(prepare_text("ştiinţă"), "ȘTIINȚĂ")
        with self.assertRaises(ValueError):
            prepare_text("lab1")

    def test_round_trip_all_keys(self):
        text = prepare_text("Învățământul românesc își păstrează țelurile")
        alphabet = permuted_alphabet(prepare_text("criptografie"))
        self.assertEqual(sorted(alphabet), sorted(ALPHABET))
        for key in range(1, N):
            self.assertEqual(decrypt(encrypt(text, key), key), text)
            self.assertEqual(decrypt(encrypt(text, key, alphabet), key, alphabet), text)


if __name__ == "__main__":
    unittest.main()
