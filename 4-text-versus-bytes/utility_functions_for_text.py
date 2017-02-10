"""
Utility functions for normalized Unicode string comparison.
Using Normal Form C, case sensitive:
>>> s1 = 'café'
>>> s2 = 'cafe\u0301'
>>> s1 == s2
False
>>> nfc_equal(s1, s2)
True
>>> nfc_equal('A', 'a')
False
Using Normal Form C with case folding:
>>> s3 = 'Straße'
>>> s4 = 'strasse'
>>> s3 == s4
False
>>> nfc_equal(s3, s4)
False
>>> fold_equal(s3, s4)
True
>>> fold_equal(s1, s2)
True
>>> fold_equal('A', 'a')
True
"""
from unicodedata import normalize, combining
import string


def nfc_equal(str1, str2):
    return normalize('NFC', str1) == normalize('NFC', str2)


def fold_equal(str1, str2):
    return (normalize('NFC', str1).casefold() ==
            normalize('NFC', str2).casefold())


def shave_marks(txt):
    """Remove all diactric marks"""
    norm_text = normalize('NFD', txt)
    shaved = ''.join(c for c in norm_text
                     if not combining(c))
    return normalize('NFC', shaved)


def shave_marks_latin(txt):
    """Remove all diacritic marks from Latin base characters"""
    norm_txt = normalize('NFD', txt)
    latin_base = False
    keepers = []
    for c in norm_txt:
        if combining(c) and latin_base:
            continue # ignore diacritic on Latin base char
        keepers.append(c)
        # if it isn't combining char, it's a new base char
        if not combining(c):
            latin_base = c in string.ascii_letters
    shaved = ''.join(keepers)
    return normalize('NFC', shaved)