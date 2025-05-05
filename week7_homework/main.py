import argparse
import encryption_decryption_functions

def main(args):
    if args.choice=='d':
        decode=True
    else:
        decode=False

    encryption_decryption_functions.encode_decode_file(args.input_file, args.output_file, args.code_choice, decode=decode, n=args.shift)

if __name__=='__main__':
    parser = argparse.ArgumentParser("Parser for message encryption")
    parser.add_argument("--choice", choices=['e', 'd'], default='d', help="-e -d choice of options either decryption or encryption")
    parser.add_argument("--code_choice", choices=['c', 'm'], default='c', help="-c Ceasar cipher, -m Morse code")
    parser.add_argument("--shift", type=int, default=1,
        help="Shift value for Caesar cipher (required if using Caesar)")
    parser.add_argument("--input_file", nargs="?", default="test_caeser_decode.txt", help="input file for encryption/decryption", type=str)
    parser.add_argument("--output_file", nargs="?", default="test_caeser_encode.txt", help="output file for encryption/decryption", type=str)
    args = parser.parse_args()
    main(args)