#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
