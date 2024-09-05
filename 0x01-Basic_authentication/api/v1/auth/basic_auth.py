#!/usr/bin/env python3
""" Module for user credential management. """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """The class to manage user credentials with base64 encoding."""
    pass
