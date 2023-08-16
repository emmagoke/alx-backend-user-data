#!/usr/bin/env python3
"""
This script contains route and handles user request using flask
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    """ This handles request sent to the home route. """
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
