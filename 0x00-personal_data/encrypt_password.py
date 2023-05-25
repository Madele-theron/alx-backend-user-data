#!/usr/bin/env python3
"""Encrypting passwords
"""
import bcrypt


def hash_password(password: str = '') -> bytes:
    """
    Args: password: str to hash
    Returns the hashed password
    """
    hashed_pswd = bcrypt.hashpw(password.encode('utf-8'),
                                bcrypt.gensalt(prefix=b"2b"))

    return hashed_pswd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks validaty of password
    Args:
        hashed_password:
        password: str to hash / encrypt
    Return:
        True is i'ts valid, else false
    """
    valid_pswd = bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    return valid_pswd
