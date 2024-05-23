#!/usr/bin/env python3
""" Module for API authentication management """
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    """Class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to check if a path requires authentication
        Args:
            path (str): the path to check
            excluded_paths(List[str]): list of paths not require authentication
        Returns:
            bool: True if the path requires authentication, False otherwise
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

        if path[-1] != "/":
            path += "/"

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False

        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None):
        """
        Method to get the authorization header from the request
        Args:
            request (Flask request): the request object
        Returns:
            str: the value of the Authorization header or None if not present
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """Method to get the current user from the request"""
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request """
        if request is None:
            return None

        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
