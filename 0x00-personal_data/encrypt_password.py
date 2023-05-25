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
