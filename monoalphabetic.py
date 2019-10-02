from string import letters
from random import shuffle


def generate_mapping(pool=None):
    """Generate a Monoalphabetic Cipher"""
    if pool is None:
        pool = letters
    original_pool = list(pool)
    shuffled_pool = list(pool)
    shuffle(shuffled_pool)
    return dict(zip(original_pool, shuffled_pool))


def generate_inv_mapping(alphabet_map):
    """Given a Monoalphabetic Cipher (dictionary) return the inverse."""
    inv_alphabet_map = {}
    for key, value in alphabet_map.iteritems():
        inv_alphabet_map[value] = key
    return inv_alphabet_map


def encrypt(message, alphabet_map):
    encrypted_message = []
    for letter in message:
        encrypted_message.append(alphabet_map.get(letter, letter))
    return ''.join(encrypted_message)


def decrypt(encrypted_message, alphabet_map):
    return encrypt(
        encrypted_message,
        generate_inv_mapping(alphabet_map)
    )


def alpha_to_string(alphabet_map):
    x = '['
    for i in alphabet_map:
        x = x + i + ':' + alphabet_map.get(i)+','
    x = x + ']'
    return x
