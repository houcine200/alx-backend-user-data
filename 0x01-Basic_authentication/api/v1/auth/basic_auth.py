#!/usr/bin/env python3
""" Module for Basic Authentication """
from .auth import Auth
from models.user import User
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 part of the Authorization header.

        Args:
            base64_authorization_header (str):
            The Base64 part of the Authorization header.

        Returns:
            str: The decoded value of the Base64 string as a UTF-8 string.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts the user email and password from the Base64 decoded value.

        Args:
            decoded_base64_authorization_header (str):
            The Base64 decoded value.

        Returns:
            tuple: The user email and password.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header.split(":")[1]
        return email, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> User:
        """
        Retrieves the User instance based on the email and password.

        Args:
            user_email (str): The user email.
            user_pwd (str): The user password.

        Returns:
            User: The User instance if found, else None.
        """
        if user_email is None or not isinstance(user_email, str) or \
                user_pwd is None or not isinstance(user_pwd, str):
            return None

        user = User().search({"email": user_email})
        if user == [] or not user[0].is_valid_password(user_pwd):
            return None
        return user[0]

    def current_user(self, request=None) -> User:
        """Retrieve the User instance for a request."""
        # Extract the Authorization header from the request
        authorization_header = self.authorization_header(request)

        # Extract and decode the Base64 encoded part of the Authorization
        # header
        base64_authorization_header = self.extract_base64_authorization_header(
            authorization_header)

        # Decode the Base64 string to UTF-8
        decoded_credentials = self.decode_base64_authorization_header(
            base64_authorization_header)

        # Extract user credentials from the decoded string
        email, password = self.extract_user_credentials(decoded_credentials)

        # Retrieve the User object based on the extracted credentials
        user = self.user_object_from_credentials(email, password)

        return user
