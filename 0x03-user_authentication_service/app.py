#!/usr/bin/env python3
"""
This script contains route and handles user request using flask
"""
from flask import Flask, jsonify, request, abort
from auth import Auth


Auth = Auth()
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    """ This handles request sent to the home route. """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ This handles the post request of the users route. """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user_register = Auth.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")