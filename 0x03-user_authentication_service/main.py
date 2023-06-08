#!/usr/bin/env python3
""" Module for End-to-end integration tests"""
import requests

URL = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ Method to register a new user

        args:
            email: user email
            password: user pswd
    """
    user_data = {
        "email": email,
        "password": password,
    }
    response = requests.post(f'{URL}/users', data=user_data)
    message = {"email": EMAIL, "message": "user created"}

    assert response.status_code == 200
    assert response.json() == message


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test to validate wrong pswd login
    """
    user_data = {
        "email": email,
        "password": password,
    }
    response = requests.post(f'{URL}/sessions', data=user_data)

    assert response.status_code == 401


def profile_unlogged() -> None:
    """ Test profile validation wihtout logging in
    """
    response = requests.delete(f'{URL}/sessions')

    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """ Test successful login
    """
    user_data = {
        "email": email,
        "password": password,
    }
    response = requests.post(f'{URL}/sessions', data=user_data)

    message = {
        "email": email,
        "message": "logged in"
    }
    assert response.status_code == 200
    assert response.json() == message

    return (response.cookies['session_id'])


def profile_logged(session_id: str) -> None:
    """ Test for profile login request
    """
    cookies = {
        "session_id": session_id
    }
    response = requests.get(f'{URL}/profile', cookies=cookies)

    message = {
        "email": EMAIL,
    }

    assert response.status_code == 200
    assert response.json() == message


def log_out(session_id: str) -> None:
    """ Test endpoint for log out
    """
    cookies = {
        "session_id": session_id
    }
    response = requests.delete(f'{URL}/sessions', cookies=cookies)

    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """ Test valid reset token
    """
    user_data = {
        "email": email
    }
    response = requests.post(f'{URL}/reset_password', data=user_data)

    token = response.json().get('reset_token', None)
    message = {"email": email, "reset_token": token}

    assert response.status_code == 200
    assert response.json() == message

    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test for valid passwordd update token
    """
    user_data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password,
    }
    response = requests.put(f'{URL}/reset_password', data=user_data)

    message = {"email": email, "message": "Password updated"}

    assert response.status_code == 200
    assert response.json() == message


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
