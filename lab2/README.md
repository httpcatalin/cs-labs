# Lab 2 - Cryptanalysis of monoalphabetic ciphers

Breaking a monoalphabetic substitution cipher (variant 7) with frequency analysis.

Run the tool on the ciphertext:

```
python3 frequency_analysis.py ciphertext.txt
```

Commands: `V=e W=t` (substitute), `V=` (remove), `show`, `freq`, `words`, `key`, `plain`, `help`, `quit`.

Tests:

```
python3 -m unittest -v test_frequency_analysis
```

Decrypted text: `plaintext.txt`. Report: `report.pdf`
