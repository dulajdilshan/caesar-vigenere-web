from string import ascii_lowercase as lowers


def alphabet_position(letter):
    assert len(letter) == 1, 'Only give me one letter please'
    return lowers.index(letter.lower())


def rotate_character(char, rot=1):
    if char.isalpha():
        origin_pos = alphabet_position(char)
        new_pos = (origin_pos + rot) % 26
        new_char = lowers[new_pos]
        return new_char if char.islower() else new_char.upper()
    else:
        return char
