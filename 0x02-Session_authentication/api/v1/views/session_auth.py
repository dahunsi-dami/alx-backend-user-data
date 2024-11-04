#!/usr/bin/env python3
"""Flask view that handles all routes for Session authentication."""

from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """Handles the session authentication login route."""

    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    if not session_id:
        return jsonify({"error": "unable to create session"}), 500

    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response