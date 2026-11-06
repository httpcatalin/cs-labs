import unicodedata

ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
LOWERCASE = "aăâbcdefghiîjklmnopqrsștțuvwxyz"
MATRIX_ALPHABET = ALPHABET.replace("Q", "")
COLUMNS = 6
MIN_KEY_LENGTH = 7
LETTERS = "Romanian letters (A-Z, a-z, Ă, Â, Î, Ș, Ț)"

UPPER_OF = {}
for i in range(len(ALPHABET)):
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
    return result.replace("Q", "K")


def build_matrix(key, alphabet=MATRIX_ALPHABET, columns=COLUMNS):
    letters = ""
    for ch in key + alphabet:
        if ch in alphabet and ch not in letters:
            letters += ch
    return [letters[i:i + columns] for i in range(0, len(letters), columns)]


def make_pairs(text):
    pairs = []
    i = 0
    while i < len(text):
        first = text[i]
        if i + 1 < len(text) and text[i + 1] != first:
            pairs.append(first + text[i + 1])
            i += 2
        else:
            pairs.append(first + ("Z" if first == "X" else "X"))
            i += 1
    return pairs


def transform_pair(pair, matrix, step):
    position = {letter: (r, c) for r, row in enumerate(matrix) for c, letter in enumerate(row)}
    (r1, c1), (r2, c2) = position[pair[0]], position[pair[1]]
    rows, columns = len(matrix), len(matrix[0])
    if r1 == r2:
        return matrix[r1][(c1 + step) % columns] + matrix[r2][(c2 + step) % columns]
    if c1 == c2:
        return matrix[(r1 + step) % rows][c1] + matrix[(r2 + step) % rows][c2]
    return matrix[r1][c2] + matrix[r2][c1]


def encrypt(text, matrix):
    return [transform_pair(pair, matrix, 1) for pair in make_pairs(text)]


def decrypt(text, matrix):
    pairs = [text[i:i + 2] for i in range(0, len(text), 2)]
    return [transform_pair(pair, matrix, -1) for pair in pairs]


def ciphertext_error(text):
    if len(text) % 2 == 1:
        return f"The ciphertext must have an even number of letters (it has {len(text)})."
    for i in range(0, len(text), 2):
        if text[i] == text[i + 1]:
            return f"The pair '{text[i:i + 2]}' (letters {i + 1}-{i + 2}) cannot appear in a Playfair ciphertext."
    return None


def read_option(prompt, options):
    while True:
        value = input(prompt).strip().lower()
        if value in options:
            return value
        print(f"Invalid option '{value}'. Allowed options: {', '.join(options)}.")


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


def read_key():
    while True:
        key = read_text(f"Key (at least {MIN_KEY_LENGTH} letters): ")
        if len(key) >= MIN_KEY_LENGTH:
            return key
        print(f"Key too short ({len(key)} letters). It must have at least {MIN_KEY_LENGTH} letters.")


def read_ciphertext():
    while True:
        text = read_text("Ciphertext: ")
        error = ciphertext_error(text)
        if not error:
            return text
        print(error)


def print_matrix(matrix):
    print("Matrix:")
    for row in matrix:
        print("   " + " ".join(row))


def main():
    print(f"Playfair cipher for the Romanian alphabet ({len(MATRIX_ALPHABET) // COLUMNS} x {COLUMNS} matrix, Q is written as K)")
    while True:
        print()
        print("1 - Encrypt")
        print("2 - Decrypt")
        print("0 - Exit")
        option = read_option("Choose: ", ["1", "2", "0"])
        if option == "0":
            break
        matrix = build_matrix(read_key())
        print_matrix(matrix)
        if option == "1":
            text = read_text("Message: ")
            print("Pairs:", " ".join(make_pairs(text)))
            print("Ciphertext:", "".join(encrypt(text, matrix)))
        else:
            text = read_ciphertext()
            pairs = decrypt(text, matrix)
            print("Decrypted pairs:", " ".join(pairs))
            print("Decrypted text:", "".join(pairs))


if __name__ == "__main__":
    main()
