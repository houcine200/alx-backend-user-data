#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from api.v1.views import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    """
    Handle user login
    Return:
        dictionary representation of user if found else error message
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate email and password
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    # Retrieve users based on email
    users = User.search({"email": email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404

    # Loop through users to find a matching password
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            # Create session ID for the user
            session_id = auth.create_session(user.id)

            # Set cookie in the response
            response = jsonify(user.to_json())
            # Retrieve the SESSION_NAME environment variable
            session_name = os.getenv('SESSION_NAME')
            response.set_cookie(session_name, session_id)
            return response

    # If password does not match any user
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_logout():
    """Logout route."""
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
