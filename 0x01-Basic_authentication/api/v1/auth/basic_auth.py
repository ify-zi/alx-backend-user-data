#!/usr/bin/env python3
"""
    Module for the Basic Authentication
"""
from api.v1.auth.auth import Auth


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
