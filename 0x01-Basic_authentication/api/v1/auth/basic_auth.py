#!/usr/bin/env python3
""" Module for user credential management. """
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """The class to manage user credentials with base64 encoding."""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:  # noqa: E501
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

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:  # noqa: E501
        """
        Gets decoded value of a Base64 string.

        Returns:
            - None if base64_authorization_header is None.
            - None if base64_authorization_header is not a string.
            - None if base64_authorization_header not valid Base64,
            using try/except block.
            - Otherwise, decoded value as UTF8 string w/ decode('utf-8').
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decode_val = base64.b64decode(base64_authorization_header)
            return decode_val.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None
