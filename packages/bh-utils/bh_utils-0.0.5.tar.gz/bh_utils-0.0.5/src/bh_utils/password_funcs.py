"""
Some password routines.

For usage examples, see ``./tests/test_password_funcs.py``.
"""

import string
import random
import secrets

def generate_password(min_length: int, max_length: int) -> str:
    """Generate a random password of symbols, digits and letters. The length is
    random within ``min_length`` and ``max_length``.

    Source: https://geekflare.com/password-generator-python-code/

    :param int min_length: password random min length.
    :param int max_length: password random max length.

    :return: a password of length between ``min_length`` and ``max_length``, \
        consists of symbols, digits and letters.
    :rtype: str.    
    """

    # Define the alphabet.
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation

    alphabet = letters + digits + special_chars

    # Random password length between min_length and max_length.
    pwd_length = random.randint(min_length, max_length)

    # Generate password meeting constraints.
    while True:
        pwd = ''

        for i in range(pwd_length):
            pwd += ''.join(secrets.choice(alphabet))

        if (any(char in special_chars for char in pwd) and 
            sum(char in digits for char in pwd)>=2):
            break

    return pwd