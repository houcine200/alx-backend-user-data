#!/usr/bin/env python3
""" script to hash passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and returns the hashed password.
    Args:
        password (str): The password to be hashed.
    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed
