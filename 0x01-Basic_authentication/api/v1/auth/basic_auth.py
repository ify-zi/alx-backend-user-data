#!/usr/bin/env python3
"""
    Module for the Basic Authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode as dec


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
