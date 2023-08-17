#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """returns a json response"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", strict_slashes=False, methods=["POST"])
def users():
    """user function"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        user_exist = AUTH._db.find_user_by(email=email)
    except NoResultFound:
        user = AUTH.register_user(email, password)
        value = {
            "email": "{}".format(user.email),
            "message": "user created"}
        return jsonify(value), 200
    return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", strict_slashes=False, methods=["POST"])
def login():
    """login function"""
    email = request.form.get("email")
    password = request.form.get("password")
    user = AUTH.valid_login(email, password)
    if not user:
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        value = {
            "email": "{}".format(email),
            "message": "logged in"}
        response = jsonify(value)
        response.set_cookie("session_id", session_id)
        return response


@app.route("/sessions", strict_slashes=False, methods=["DELETE"])
def logout():
    """logout function"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None or session_id is None:
        abort(403)
    else:
        AUTH.destroy_session(user.id)
        return redirect("/")


@app.route("/profile", strict_slashes=False)
def profile():
    """profile function"""
    session_id = request.cookies.get(session_id)
    user = AUTH._db.find_user_by(session_id=session_id)
    if not user:
        abort(403)
    return jsonify({"email": "{}".format(user.email)}), 200


@app.route("/reset_password", strict_slashes=False, methods=["POST"])
def get_reset_password_token():
    """Get reset password token"""
    email = request.form.get("email")
    user = AUTH._db.find_user_by(email=email)
    if not user:
        abort(403)
    token = AUTH.get_reset_password_token(email)
    value = {
        "email": "{}".format(email),
        "reset_token": "{}".format(token)}
    return jsonify(value), 200


@app.route("/reset_password", strict_slashes=False, methods=["PUT"])
def update_password():
    """update password function"""
    email = request.form.get("email")
    new_passwd = request.form.get("new_password")
    reset_token = request.form.get("reset_token")
    try:
        AUTH.update_password(reset_token, new_passwd)
    except valueError:
        abort(403)

    return jsonify({"email": f"{email}", "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
