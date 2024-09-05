#!/usr/bin/env python3
""" Module for user credential management. """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """The class to manage user credentials with base64 encoding."""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Gets base64 part of Authorization header-
        -for a basic authentication.

        Returns:
            - None if authorization_header is None.
            - None if authorization_header isn't a string.
            - None if authorization_header doesn't start by 'Basic '.
            - Otherwise, value after 'Basic '.

        Assume authorization_header contains only one Basic.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]
