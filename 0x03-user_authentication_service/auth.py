#!/usr/bin/env python3
import bcrypt

def _hash_password(password: str) -> bytes:
    """
    Hashes a password string using bcrypt.
    """
    password_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password