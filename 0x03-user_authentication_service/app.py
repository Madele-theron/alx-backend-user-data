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


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """Generate logging in response
    """
    email = request.form.get('email')
    pswd = request.form.get('password')

    if email is None or pswd is None:
        abort(401)

    if AUTH.valid_login(email=email, password=pswd) is False:
        abort(401)
    session = AUTH.create_session(email=email)
    if session is not None:
        response = jsonify({'email': email, 'message': 'logged in'})
        response.set_cookie("session_id", session)
        return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Logs out a user / session
    """
    session = request.cookies.get('session_id', None)
    if session is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/', code=302)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """Get user profile
    """
    session = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(session)

    if session is None or user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def reset_password() -> str:
    """reset the password of user
    """
    try:
        email = request.form.get('email')
    except KeyError:
        abort(401)

    try:
        token: str = AUTH.get_reset_password_token(email=email)
    except ValueError:
        abort(403)

    return jsonify(
        {"email": email, "reset_token": token}
        ), 200


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """Route - Update user password
    """
    try:
        email = request.form.get('email')
        pswd = request.form.get('new_password')
        token = request.form.get('reset_token')
    except KeyError:
        abort(401)

    try:
        AUTH.update_password(token, pswd)
    except ValueError:
        abort(403)

    return jsonify(
        {"email": f"{email}", "message": "Password updated"}
        ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
