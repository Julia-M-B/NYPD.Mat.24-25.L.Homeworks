import sys
import numpy as np

def cosinus(args):
    if not args:
        raise ValueError("Invalid number of arguments")
    try:
        x = np.array(args).astype(np.float32)
        return np.cos(x).flatten()
    except ValueError as e:
        print("Invalid argument(s).")
        print(e)
        sys.exit(1)


def main():
    try:
        print(*cosinus(sys.argv[1:]))
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()