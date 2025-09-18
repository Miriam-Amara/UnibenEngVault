#!/usr/bin/env python3

"""
"""

from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Request, abort
from typing import cast
import logging
import os

from api.v1.auth.auth import Auth
from api.v1.utils import get_obj
from models.user import User
from models.user_session import UserSession


load_dotenv()
logger = logging.getLogger(__name__)


class SessionDBAuth(Auth):
    """
    """
    def __init__(self) -> None:
        """
        """
        self.session_duration = int(os.getenv("SESSION_DURATION", 0))

    def create_session(self, user_id: str | None=None) -> str | None:
        """
        """
        if not user_id or not isinstance(user_id, str): # type: ignore
            return
        
        user_session = UserSession(user_id=user_id)
        try:
            user_session.save()
        except Exception as e:
            logger.error(f"Database operation failed: {e}")
            abort(500)

        return user_session.id
    
    def current_user(self, request: Request | None=None) -> User | None:
        """
        """
        logger.debug("In current_user")
        session_id = self.session_cookie(request)
        if not session_id:
            return
        
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return
        
        user = cast(User, get_obj("User", user_id))
        logger.debug(f"{user}")
        logger.debug(f"{user.role.value}")
        if user:
            return user

    def destroy_session(self, request: Request | None=None) -> bool | None:
        """
        """
        if not request:
            return

        session_id = self.session_cookie(request)
        if not session_id:
            return False
        
        session = cast(UserSession, get_obj("UserSession", session_id))
        if not session:
            return False
        
        try:
            session.delete()
            session.save()
        except Exception as e:
            logger.error(f"Database operation failed: {e}")
            return False
        return True

    def user_id_for_session_id(self, session_id: str | None=None) -> str | None:
        """
        """
        if not session_id or not isinstance(session_id, str): # type: ignore
            return
        session = cast(UserSession, get_obj("UserSession", session_id))
        if not session:
            return
        if self.session_duration <= 0:
            return session.user_id
        if (session.created_at + timedelta(seconds=self.session_duration)) < datetime.now():
            try:
                session.delete()
                session.save()
                logger.debug("Session expired")
            except Exception as e:
                logger.error(f"Failed to delete expired session: {e}")
                return
        logger.debug(f"{session.user_id}")
        return session.user_id
