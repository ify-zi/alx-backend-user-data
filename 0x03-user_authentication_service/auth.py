#!/usr/bin/env python3
"""
    Authentication module
"""

import bcrypt
import uuid
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """ passowrd hashing mehtod"""
    pwd = password.encode('utf-8')
    hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """genrate a string repr of the id"""
    return str(uuid.uuid4())


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
            user = self._db.add_user(email, _hash_password(password))
            return user
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """credential validation method"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return True
        else:
            return False

    def create_session(self, email: str) -> str:
        """creates user session"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                user.session_id = _generate_uuid()
                self._db._session.commit()
        except NoResultFound:
            return None
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """return user object from id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except (NoResultFound, ValueError):
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy session method"""
        if user_id is None:
            return None
        self._db.update_self(user_id, session_id=None)
