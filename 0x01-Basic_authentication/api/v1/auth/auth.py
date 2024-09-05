#!/usr/bin/env python3
""" Module for API auth management. """
from flask import request
from typing import List, TypeVar

User = TypeVar('User')


class Auth:
    """ The class to manage API authentication. """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required-
        -for the given path.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns the authorization header. """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user. """
        return None
