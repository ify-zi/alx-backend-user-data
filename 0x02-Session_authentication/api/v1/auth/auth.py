#!/usr/bin/env python3
"""
    Authentication model module
"""

import os
from flask import request
from typing import TypeVar, List


class Auth:
    """
        Class for authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """method definition"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        path = path.rstrip("/")
        for ex_path in excluded_paths:
            if ex_path.endswith("*"):
                ex_path = ex_path[:-1]
                if path.startswith(ex_path):
                    return False
            elif ex_path.rstrip("/") == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """method definitio"""
        if request is not None:
            auth_head = request.headers.get("Authorization")
            if auth_head is not None:
                return auth_head
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method definition"""
        return None

    def session_cookie(self, request=None):
        """method definition"""
        if request is None:
            return None
        _my_session_id = os.getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)
