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
def login_ses():
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


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """loging out adn session destruction"""
    session_id = request.cookies.get("session_id")
    user = Auth.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    Auth.destory_session(user.id)
    redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
