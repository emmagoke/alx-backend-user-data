#!/usr/bin/env python3
"""
This script contains route that handles things concerning authentication
"""
from flask import jsonify, request
from api.v1.views import app_views
from os import getenv
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """ This view handle user login using session authentication. """
    email = request.form.get('email')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    session_name = getenv('SESSION_NAME')
    response = jsonify(user[0].to_json())
    response.set_cookie(session_name, session_id)
    return response
