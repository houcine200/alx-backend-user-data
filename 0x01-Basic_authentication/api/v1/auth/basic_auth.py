#!/usr/bin/env python3
""" Module for Basic Authentication """
from .auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class that inherits from Auth"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of Authorization header for Basic Authent.

        Args:
            authorization_header (str): The authorization header.

        Returns:
            str: The Base64 part of the Authorization header.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        base64_part = authorization_header.split(' ')[1]
        return base64_part
