#!/usr/bin/env python3
""" Module for user credential management. """
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
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

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):  # noqa: E501
        """
        Gets user email and password from Base64 decoded value.

        Returns:
            - None, None if decoded_base64_authorization_header is None.
            - None, None if decoded_base64_authorization_header isn't str.
            - None, None if decoded_base64_authorization_header don't has ':'
            - Otherwise, email, password separated by ':'.

        Assume decoded_base64_authorization_header contains one ':'.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        details = decoded_base64_authorization_header.split(':', 1)
        if len(details) != 2:
            return None, None

        return details[0], details[1]

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):  # noqa: E501
        """
        Gets user instance based on his/her email & password.

        Returns:
            - None if user_email is Nonen or not a string.
            - None if user_pwd is None or not a string.
            - None if db contains no User instance with user_email.
            - None if user_pwd is not password of User instance found.
            - Otherwise, User instance.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        user_list = User.search({'email': user_email})
        if not user_list:
            return None

        user = user_list[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user
