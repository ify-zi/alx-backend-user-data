#!/usr/bin/env python3
"""
    Flask module, API declaration
"""

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def home():
    """route views that return payload"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def login():
    """ login api"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email,
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"})


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login_ses() -> str:
    """login api for sesssion"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": email,
                        "message": "logged in"})
        resp.set_cookie("session_id", session_id)
        return resp
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """loging out adn session destruction"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def get_profile() -> str:
    """Method return user details or profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ Reset password route """
    try:
        email = request.form.get('email')
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify(email=email, reset_token=reset_token)
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """ Reset password route """
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')

        AUTH.update_password(reset_token, new_password)
        return jsonify(email=email, message="Password updated")
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
