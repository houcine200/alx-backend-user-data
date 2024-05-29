#!/usr/bin/env python3
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """
    GET route that returns a JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """
    POST route to register a new user.

    Expects form data with 'email' and 'password' fields.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login():
    """log in"""
    email, password = request.form.get("email"), request.form.get("password")
    if AUTH.valid_login(email, password):
        session_ID = AUTH.create_session(email)
        responce = make_response({"email": email, "message": "logged in"})
        responce.set_cookie("session_id", session_ID)
        return responce
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
