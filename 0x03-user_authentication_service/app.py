#!/usr/bin/env python3
""" Flask module """
from flask import Flask, jsonify, request, abort, redirect, make_response
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@ app.route('/', methods=['GET'])
def main() -> str:
    """ Message """
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route("/users", methods=['POST'], strict_slashes=False)
def register_user():
    """End point to register a user"""
    email = request.form.get('email')
    pswd = request.form.get('password')

    if email is None or pswd is None:
        abort(400)

    try:
        user = AUTH.register_user(email, pswd)
    except ValueError:
        message = {"message": "email already registered"}
        return jsonify(message), 400

    else:
        return jsonify({
            "email": f"{user.email}",
            "message": "user created"
        }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
