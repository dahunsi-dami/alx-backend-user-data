#!/usr/bin/env python3
""" Module for API auth management. """
from flask import request
from typing import List, TypeVar
import os

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

        for removed_path in excluded_paths:
            removed_path = removed_path.rstrip('/')
            if path == removed_path:
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

    def session_cookie(self, request=None):
        """
        Gets a cookie value from a request.

        Returns:
            - None if request is None
            - Value of cookie named _my_session_id from request.

        Name of cookie must be defined by env variable SESSION_NAME.
        Must use env variable SESSION_NAME to define name of-
        -cookie used for the Session ID.
        """
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")

        if session_name is None:
            return None

        return request.cookies.get(session_name)
