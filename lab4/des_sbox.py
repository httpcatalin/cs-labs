import random

SBOXES = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ],
]
HEX_DIGITS = "0123456789abcdefABCDEF"


def parse_bits(text):
    value = text.replace(" ", "")
    if len(value) == 48:
        for ch in value:
            if ch not in "01":
                raise ValueError(f"Invalid character '{ch}'. A 48-character input may contain only 0 and 1.")
        return value
    if len(value) == 12:
        for ch in value:
            if ch not in HEX_DIGITS:
                raise ValueError(f"Invalid character '{ch}'. A 12-character input must be hexadecimal (0-9, A-F).")
        return format(int(value, 16), "048b")
    raise ValueError(f"Wrong length ({len(value)} characters). Enter 48 bits (0 and 1) "
                     f"or 12 hexadecimal digits; spaces are ignored.")


def split_groups(bits):
    return [bits[i:i + 6] for i in range(0, 48, 6)]


def sbox_lookup(j, group):
    row = int(group[0] + group[5], 2)
    column = int(group[1:5], 2)
    return row, column, SBOXES[j][row][column]


def substitute(bits):
    return "".join(format(sbox_lookup(j, group)[2], "04b") for j, group in enumerate(split_groups(bits)))


def print_sbox(j, row, column):
    print(f"S{j + 1:<3}" + "".join(f"{c:5}" for c in range(16)))
    for r in range(4):
        cells = ""
        for c in range(16):
            value = SBOXES[j][r][c]
            cells += f"[{value}]".rjust(5) if (r, c) == (row, column) else f"{value:5}"
        print(f"{r:<4}" + cells)


def show_substitution(bits):
    groups = split_groups(bits)
    print("B1B2...B8 =", " ".join(groups))
    print("Hex:", format(int(bits, 2), "012X"))
    print()
    for j, group in enumerate(groups):
        row, column, value = sbox_lookup(j, group)
        print(f"B{j + 1} = {group}   row = b1b6 = {group[0]}{group[5]} = {row}   "
              f"column = b2b3b4b5 = {group[1:5]} = {column}")
        print_sbox(j, row, column)
        print(f"S{j + 1}(B{j + 1}) = S{j + 1}[{row}][{column}] = {value} = {value:04b}")
        print()
    result = substitute(bits)
    print("S1(B1)S2(B2)...S8(B8) =", " ".join(result[i:i + 4] for i in range(0, 32, 4)))
    print("Hex:", format(int(result, 2), "08X"))


def read_bits():
    while True:
        try:
            return parse_bits(input("B1B2...B8 (48 bits or 12 hex digits): "))
        except ValueError as error:
            print(error.args[0])


def read_option(prompt, options):
    while True:
        value = input(prompt).strip()
        if value in options:
            return value
        print(f"Invalid option '{value}'. Allowed options: {', '.join(options)}.")


def main():
    print("DES S-box substitution: S1(B1)S2(B2)...S8(B8) from B1B2...B8 (Task 2.7)")
    while True:
        print()
        print("1 - Enter B1B2...B8")
        print("2 - Generate B1B2...B8 at random")
        print("0 - Exit")
        option = read_option("Choose: ", ["1", "2", "0"])
        if option == "0":
            break
        if option == "1":
            bits = read_bits()
        else:
            bits = format(random.getrandbits(48), "048b")
            print("Generated:", bits)
        print()
        show_substitution(bits)


if __name__ == "__main__":
    main()
