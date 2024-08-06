#!/usr/bin/env python3
"""
    Module for the Basic Authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode as dec
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
        BasicAuth class defintion and its methods
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """method that extract the authorization details from
            auth header
        """
        if authorization_header is not None:
            if isinstance(authorization_header, str):
                if authorization_header.startswith('Basic '):
                    return authorization_header[6:]
        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
            Method to conver the base64 encode to str
        """
        if base64_authorization_header is not None:
            if isinstance(base64_authorization_header, str):
                try:
                    return dec(base64_authorization_header).decode('utf-8')
                except Exception:
                    return None
        return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ Credential Extraction method"""
        if decoded_base64_authorization_header is not None:
            if isinstance(decoded_base64_authorization_header, str):
                s_point = decoded_base64_authorization_header.find(':')
                if s_point > 0:
                    username = decoded_base64_authorization_header[:s_point]
                    cred = decoded_base64_authorization_header[s_point + 1:]
                    return (username, cred)
        return (None, None)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ retrns the User Object"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if len(users) == 0:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the current"""
        auth_header = self.authorization_header(request)
        auth_header_val = self.extract_base64_authorization_header(auth_header)
        decoded_val = self.decode_base64_authorization_header(auth_header_val)
        credentials = self.extract_user_credentials(decoded_val)
        usr_email = credentials[0]
        usr_pwd = credentials[1]
        return self.user_object_from_credentials(usr_email, usr_pwd)
