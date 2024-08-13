#!/usr/bin/env python3
"""
    Authentication module
"""

from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import bcrypt


def _hash_password(password: str) -> bytes:
    """ passowrd hashing mehtod"""
    pwd = password.encode('utf-8')
    hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """constructor function"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """method creates user if user exist
            Args: email: str, password: str
            Return: created User object
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            self._db.add_user(email, _hash_password(password))
        raise ValueError("User {:s} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """credential validation method"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            pass
        if bcrypt.checkpw(password, user.hash_password):
            return True
        else:
            return False
