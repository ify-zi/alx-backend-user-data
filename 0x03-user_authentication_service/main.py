#!/usr/bin/env python3
""" Tests Suite """

import requests


BASE_URL = "http://127.0.0.1:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ Test case for register_user function """
    data = {'email': email, 'password': password}
    r = requests.post(f'{BASE_URL}/users', data=data)

    success = {"email": email, "message": "user created"}
    failure = {"message": "email already registered"}

    if r.status_code == 200:
        assert(r.json() == success)
    else:
        assert(r.status_code == 400)
        assert(r.json() == failure)


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test case for login with wrong password """
    data = {'email': email, 'password': password}
    r = requests.post(f'{BASE_URL}/sessions', data=data)

    assert(r.status_code == 401)


def log_in(email: str, password: str) -> str:
    """ Test case for successful login """
    data = {'email': email, 'password': password}
    r = requests.post(f'{BASE_URL}/sessions', data=data)

    success = {"email": email, "message": "logged in"}

    assert(r.status_code == 200)
    assert(r.json() == success)
    return r.cookies.get('session_id')


def profile_unlogged() -> None:
    """ Test case for User with no session_id """
    cookies = {'session_id': 'fake'}
    r = requests.get(f'{BASE_URL}/profile', cookies=cookies)

    assert(r.status_code == 403)


def profile_logged(session_id: str) -> None:
    """ Test case for user with session_id """
    cookies = {'session_id': session_id}
    r = requests.get(f'{BASE_URL}/profile', cookies=cookies)

    assert(r.status_code == 200)


def log_out(session_id: str) -> None:
    """ Test case for logging out user from session """
    cookies = {'session_id': session_id}
    r = requests.delete(f'{BASE_URL}/sessions', cookies=cookies)

    assert(r.url == f'{BASE_URL}/')


def reset_password_token(email: str) -> str:
    """ Test case for password reset token generation """
    data = {'email': email}
    r = requests.post(f'{BASE_URL}/reset_password', data=data)

    if r.status_code == 200:
        res = r.json()
        success = {"email": email, "reset_token": res.get('reset_token')}
        assert(res == success)
        return res.get('reset_token')
    else:
        assert(r.status_code == 403)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test case for updating password with reset token """
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    r = requests.put(f'{BASE_URL}/reset_password', data=data)

    success = {"email": email, "message": "Password updated"}

    if r.status_code == 200:
        assert(r.json() == success)
    else:
        assert(r.status_code == 403)


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
