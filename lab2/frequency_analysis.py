import re
import string
import sys
from collections import Counter

ENGLISH = {
    "A": 8.17, "B": 1.49, "C": 2.78, "D": 4.25, "E": 12.70, "F": 2.23, "G": 2.01,
    "H": 6.09, "I": 6.97, "J": 0.15, "K": 0.77, "L": 4.03, "M": 2.41, "N": 6.75,
    "O": 7.51, "P": 1.93, "Q": 0.09, "R": 5.99, "S": 6.33, "T": 9.06, "U": 2.76,
    "V": 0.98, "W": 2.36, "X": 0.15, "Y": 1.97, "Z": 0.07,
}
UPPER = string.ascii_uppercase
LETTERS = string.ascii_letters

HELP = """Commands:
  V=e W=t    substitute cipher letter V with e and W with t (V= removes V)
  show       show the text with the current substitutions
  freq       letter frequencies of the ciphertext compared with English
  words      most common 1, 2 and 3 letter words of the ciphertext
  key        show the current key
  plain      show the decrypted text (only when every letter is known)
  help       show this list
  quit       exit"""


# V=e W=t Q=h T=a X=i P=s G=n O=d N=o C=f R=w H=c U=p I=r F=y S=l J=g D=u Z=m A=b K=v Y=x L=k E=j B=q M=z

def letter_frequencies(text):
    counts = Counter(ch.upper() for ch in text if ch in LETTERS)
    total = sum(counts.values())
    table = [(letter, counts[letter], 100 * counts[letter] / total) for letter in UPPER]
    return sorted(table, key=lambda row: (-row[1], row[0])) #dupa count desc


def english_order():
    return sorted(UPPER, key=lambda letter: -ENGLISH[letter]) #sortat pe frecv


def common_words(text, length, top=5):
    words = [word.upper() for word in re.findall(r"[A-Za-z]+", text) if len(word) == length]
    return Counter(words).most_common(top)


def apply_key(text, key):
    result = ""
    for ch in text:
        if ch in LETTERS and ch.upper() in key:
            result += key[ch.upper()]
        elif ch in LETTERS:
            result += ch.upper()
        else:
            result += ch
    return result


def decrypt(text, key):
    result = ""
    for ch in text:
        if ch in string.ascii_uppercase:
            result += key[ch].upper()
        elif ch in string.ascii_lowercase:
            result += key[ch.upper()]
        else:
            result += ch
    return result


def add_pairs(key, command):
    pairs = command.split()
    for pair in pairs:
        if not re.fullmatch(r"[A-Za-z]=[A-Za-z]?", pair):
            return f"Invalid command '{pair}'. Use CIPHER=plain, for example V=e (V= removes it). Type help."
    new_key = dict(key)
    for pair in pairs:
        cipher, plain = pair[0].upper(), pair[2:].lower()
        new_key.pop(cipher, None)
        if not plain:
            continue
        for other, value in new_key.items():
            if value == plain:
                return f"'{plain}' is already the image of {other}. Remove it first with {other}="
        new_key[cipher] = plain
    key.clear()
    key.update(new_key)
    return None


def print_frequencies(text):
    english = english_order()
    print("Rank  Cipher  Count       %  |  English       %")
    for rank, (letter, count, percent) in enumerate(letter_frequencies(text)):
        print(f"{rank + 1:4}  {letter:>6}  {count:5}  {percent:6.2f}  |  {english[rank]:>7}  {ENGLISH[english[rank]]:6.2f}")


def print_words(text):
    for length in (1, 2, 3):
        found = ", ".join(f"{word} ({count})" for word, count in common_words(text, length))
        print(f"{length}-letter words: {found}")


def print_key(key):
    print("cipher: " + " ".join(UPPER))
    print("plain:  " + " ".join(key.get(letter, ".") for letter in UPPER))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "ciphertext.txt"
    with open(path, encoding="utf-8") as file:
        text = file.read()
    key = {}
    print_frequencies(text)
    print(HELP)
    while True:
        command = input("> ").strip()
        if not command:
            continue
        elif command == "quit":
            break
        elif command == "help":
            print(HELP)
        elif command == "freq":
            print_frequencies(text)
        elif command == "words":
            print_words(text)
        elif command == "show":
            print(apply_key(text, key))
        elif command == "key":
            print_key(key)
        elif command == "plain":
            missing = sorted({ch.upper() for ch in text if ch in LETTERS} - set(key))
            if missing:
                print("The key is not complete yet. Unknown cipher letters: " + " ".join(missing))
            else:
                print(decrypt(text, key))
        else:
            error = add_pairs(key, command)
            if error:
                print(error)
            else:
                print(apply_key(text, key))


if __name__ == "__main__":
    main()
