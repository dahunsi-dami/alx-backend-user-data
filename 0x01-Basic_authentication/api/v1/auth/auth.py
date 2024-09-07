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

        Returns:
            - True if path is None
            - True if excluded_paths is None/empty
            - False if path is in excluded_paths

        Is slash tolerant. That is, path=/api/v1/status and-
        -path=/api/v1/status/ must return False if excluded_paths-
        -contains /api/v1/status/
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path.rstrip('/')

        for excl_path in excluded_paths:
            excl_path = excl_path.rstrip('/')
            if path == excl_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header.

        Returns:
            - None if request is None
            - None if request don't contain header key Authorization
            - Otherwise, value of header request Authorization
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user. """
        return None
