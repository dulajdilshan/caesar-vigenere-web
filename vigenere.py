from helpers import alphabet_position, rotate_character
from sys import exit


def encrypt(text, key):
    i = 0
    key_mod = len(key)
    ciphertext = ''
    for char in text:
        if char.isalpha():
            ciphertext += rotate_character(char, alphabet_position(key[i]))
            i = (i + 1) % key_mod
        else:
            ciphertext += char
    return ciphertext


def decrypt(ciphertext, key):
    i = 0
    key_mod = len(key)
    original = ''
    for char in ciphertext:
        if char.isalpha():
            original_shift = alphabet_position(key[i])
            original += rotate_character(char, -original_shift)
            i = (i + 1) % key_mod
        else:
            original += char
    return original


def main(key, verbose, plaintext):
    msg = input('Type a message:\n') if plaintext is None else plaintext
    key = input('Encryption key:\n') if key is None else key
    if verbose:
        print('Encrypted message:')
    try:
        print(encrypt(msg, key))
    except ValueError as e:
        if str(e) != 'substring not found':
            raise
        else:
            print('--> error: {}: {}'.format(key_error, key))
            exit()


if __name__ == '__main__':
    import argparse

    key_error = "encryption key should only contain alphabetic characters--no numbers or special characters"


    def key_parse(key):
        k = key.strip()
        if not all(char.isalpha() for char in k):
            error_msg = '{}: {}'.format(key_error, k)
            raise argparse.ArgumentTypeError(error_msg)
        return k


    parser = argparse.ArgumentParser(description='encrypt plaintext with Vigenere cypher')
    parser.add_argument('keyword', nargs='?', type=key_parse,
                        help='character sequence to use as encryption key')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="increase output verbosity")
    parser.add_argument('-t', '--text', help='plaintext to encrypt', dest='text')
    args = parser.parse_args()
    main(args.keyword, args.verbose, args.text)
