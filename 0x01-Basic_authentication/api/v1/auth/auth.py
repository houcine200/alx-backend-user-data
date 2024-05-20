#!/usr/bin/env python3
""" Module for API authentication management """
from flask import request
from typing import List, TypeVar


class Auth():
    """Class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method to check if a path requires authentication"""
        return False

    def authorization_header(self, request=None) -> str:
        """Method to get the authorization header from the request"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Method to get the current user from the request"""
        return None
