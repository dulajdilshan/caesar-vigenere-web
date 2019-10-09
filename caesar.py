from assistance import rotate_character


def encrypt(text, rot):
    return ''.join(rotate_character(char, rot) for char in text)


def major_function(shift, verbose, text):
    msg = input('Type a message:\n') if text is None else text
    while True:
        try:
            rot = int(input('Rotate by:\n')) if shift is None else shift
            break
        except ValueError:
            print('error: the shift must be an integer, please try again')
            continue
    if verbose:
        print('Encrypted message:')
    print(encrypt(msg, rot))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='encrypt plaintext with Caesar cypher')
    parser.add_argument('shift', type=int, nargs='?',
                        help='distance to shift character down alphabet')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help="increase output verbosity")
    parser.add_argument('-t', '--text', help='plaintext to encrypt', dest='text')
    args = parser.parse_args()
    major_function(args.shift, args.verbose, args.text)
