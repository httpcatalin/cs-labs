import unicodedata

ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
LOWERCASE = "aăâbcdefghiîjklmnopqrsștțuvwxyz"
N = len(ALPHABET)
MIN_KEYWORD_LENGTH = 7
LETTERS = "Romanian letters (A-Z, Ă, Â, Î, Ș, Ț)"

UPPER_OF = {}
for i in range(N):
    UPPER_OF[ALPHABET[i]] = ALPHABET[i]
    UPPER_OF[LOWERCASE[i]] = ALPHABET[i]
UPPER_OF["Ş"] = "Ș"
UPPER_OF["ş"] = "Ș"
UPPER_OF["Ţ"] = "Ț"
UPPER_OF["ţ"] = "Ț"


def prepare_text(text):
    text = unicodedata.normalize("NFC", text)
    result = ""
    for ch in text:
        if ch == " ":
            continue
        if ch not in UPPER_OF:
            raise ValueError(ch)
        result += UPPER_OF[ch]
    return result


def encrypt(text, key, alphabet=ALPHABET):
    n = len(alphabet)
    result = ""
    for ch in text:
        x = alphabet.index(ch)
        result += alphabet[(x + key) % n]
    return result


def decrypt(text, key, alphabet=ALPHABET):
    n = len(alphabet)
    result = ""
    for ch in text:
        y = alphabet.index(ch)
        result += alphabet[(y - key + n) % n]
    return result


def permuted_alphabet(keyword, alphabet=ALPHABET):
    result = ""
    for ch in keyword + alphabet:
        if ch not in result:
            result += ch
    return result


def read_option(prompt, options):
    while True:
        value = input(prompt).strip().lower()
        if value in options:
            return value
        print(f"Invalid option '{value}'. Allowed options: {', '.join(options)}.")


def read_key():
    while True:
        value = input(f"Key (integer from 1 to {N - 1}): ").strip()
        if value.isascii() and value.isdigit() and 1 <= int(value) <= N - 1:
            return int(value)
        print(f"Invalid key '{value}'. "
              f"The key must be an integer from 1 to {N - 1} inclusive.")


def read_text(prompt):
    while True:
        try:
            text = prepare_text(input(prompt))
        except ValueError as error:
            print(f"Invalid character '{error.args[0]}'. Use only {LETTERS} and spaces.")
            continue
        if text:
            return text
        print("The text must contain at least one letter.")


def read_keyword():
    while True:
        value = input(f"Keyword (at least {MIN_KEYWORD_LENGTH} letters): ").strip()
        value = unicodedata.normalize("NFC", value)
        invalid = [ch for ch in value if ch not in UPPER_OF]
        if invalid:
            print(f"Invalid character '{invalid[0]}' in keyword. "
                  f"Use only {LETTERS}, no spaces.")
        elif len(value) < MIN_KEYWORD_LENGTH:
            print(f"Keyword too short ({len(value)} letters). "
                  f"It must have at least {MIN_KEYWORD_LENGTH} letters.")
        else:
            return "".join(UPPER_OF[ch] for ch in value)


def main():
    print(f"Caesar cipher for the Romanian alphabet (n = {N})")
    while True:
        print()
        print("1 - Caesar cipher (Task 1.1)")
        print("2 - Caesar cipher with permutation (Task 1.2)")
        print("0 - Exit")
        task = read_option("Choose: ", ["1", "2", "0"])
        if task == "0":
            break
        operation = read_option("Operation (e - encrypt, d - decrypt): ", ["e", "d"])
        key = read_key()
        alphabet = ALPHABET
        if task == "2":
            keyword = read_keyword()
            alphabet = permuted_alphabet(keyword)
            print("Permuted alphabet:", " ".join(alphabet))
        if operation == "e":
            text = read_text("Message: ")
            print("Prepared message:", text)
            print("Ciphertext:", encrypt(text, key, alphabet))
        else:
            text = read_text("Ciphertext: ")
            print("Decrypted message:", decrypt(text, key, alphabet))


if __name__ == "__main__":
    main()
