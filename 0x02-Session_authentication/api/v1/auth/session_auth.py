#!/usr/bin/env python3
"""
    Module of the session Authentication
"""

import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session auth class definition and methods"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """session maker using uuid module"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """user_id retriver"""
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id
