import string

MORSE_CODE_ENCODE = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ", ": "--..--",
    ".": ".-.-.-",
    "?": "..--..",
    "/": "-..-.",
    "-": "-....-",
    "(": "-.--.",
    ")": "-.--.-",
}
MORSE_CODE_DECODE = {v: k for k, v in MORSE_CODE_ENCODE.items()}
CAESAR_LETTERS = list(string.ascii_uppercase)


def encode_decode_file(
    input_file_path: str,
    output_file_path: str,
    cipher: str,
    decode: bool = True,
    n: int = 0,
) -> None:
    """
    Function for encoding/decoding message from the input file to the output file
    using Morse code or Caesar cipher.
    :param input_file_path: Path to the input file
    :param output_file_path: Path to the output file
    :param cipher: First letter of cipher that should be used,
                   i.e. `m` for Morse code and `c` for Caesar cipher
    :param decode: True if the message should be decoded,
                   False if the message should be encoded
    :param n: shift parameter; for Ceaser encryption/decryption
    :return:
    The result of this function should be encoded/decoded message written in the output file
    """
    with open(input_file_path, "r") as in_file, open(output_file_path, "w") as out_file:
        lines = in_file.readlines()
        if cipher == "m":
            for line in lines:
                line = line.strip()
                out_file.write(morse_code(line, decode=decode) + "\n")
        elif cipher == "c":
            for line in lines:
                line = line.strip()
                out_file.write(caesar_cipher(line, n=n, decode=decode) + "\n")
        else:
            raise ValueError("The `cipher` argument should be equal to `m` or `c`.")


def caesar_cipher(s: str, n: int, decode: bool = True) -> str:
    """
    Caesar cipher decoder/encoder
    :param s: Message that should be decoded/encoded
    :param n: Value of right shift for encoding message
    :param decode: True if the message should be decoded,
                   False if the message should be encoded
    :return: Encoded/decoded message
    """
    msg_chars = list(s.upper())
    n_letters = len(CAESAR_LETTERS)
    shift = n_letters - n if decode else n
    indexes = [(i + shift) % n_letters for i in range(n_letters)]
    shift_dict = {k: CAESAR_LETTERS[idx] for k, idx in zip(CAESAR_LETTERS, indexes)}
    msg = [shift_dict.get(c, " ") for c in msg_chars]
    return "".join(msg)


def morse_code(s: str, decode: bool = True) -> str:
    """
    Morse code decoder/encoder
    :param s: Message that should be decoded/encoded
    :param decode: True if the message should be decoded,
                   False if the message should be encoded
    :return: Encoded/decoded message
    """
    if decode:
        msg_chars = s.split(" ")
        msg = "".join([MORSE_CODE_DECODE.get(c, "") for c in msg_chars])
    else:
        msg_chars = list(s.upper())
        msg = " ".join([MORSE_CODE_ENCODE.get(c, "") for c in msg_chars])
    return msg


if __name__ == "__main__":
    # test
    encode_decode_file("test_caeser_decode.txt", "test_caeser_encode.txt", "c", n=1)
