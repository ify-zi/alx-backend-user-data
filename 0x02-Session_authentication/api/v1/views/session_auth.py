#!/usr/bin/env python3
"""
    Session authentication views
"""

import os
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def session_login():
    """login auth def"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            out = jsonify(user.to_json())
            out.set_cookie(os.getenv('SESSION_NAME'), session_id)
            return out
        return jsonify({"error": "wrong password"}), 401
    return jsonify({"error": "no user found for this email"}), 404

@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def end_session():
    """session destruct method"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
