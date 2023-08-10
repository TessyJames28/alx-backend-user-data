#!/usr/bin/env python3
"""New view for Session Authentication"""
from flask import Flask, request, abort, jsonify
from models.user import User
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    """session auth"""
    email = request.form.get('email')
    passwd = request.form.get('password')
    if not email or email == '':
        return jsonify({"error": "email missing"}), 400
    if not passwd or passwd == '':
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if not user or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(passwd):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    resp = jsonify(user.to_json())
    cookie_sess = getenv('SESSION_NAME')
    resp.set_cookie(cookie_sess, session_id)
    return resp
