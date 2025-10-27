#!/usr/bin/env python3

"""
"""

from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging
import os

from api.v1.auth.authentication import BaseAuth
from api.v1.utils.utility import get_obj, DatabaseOp
from models.user import User
from models.user_session import UserSession


load_dotenv()
logger = logging.getLogger(__name__)


class SessionDBAuth(BaseAuth):
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

        db = DatabaseOp()
        db.save(user_session)

        return user_session.id
    
    def current_user(self) -> User | None:
        """
        """
        session_id = self.session_cookie()
        if not session_id:
            return
        
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return
        
        user = get_obj(User, user_id)
        if user:
            return user

    def destroy_session(self) -> bool | None:
        """
        """
        session_id = self.session_cookie()
        if not session_id:
            return False
        
        session = get_obj(UserSession, session_id)
        if not session:
            return False
        
        db = DatabaseOp()
        db.delete(session)
        db.commit()
        
        return True

    def user_id_for_session_id(self, session_id: str | None=None) -> str | None:
        """
        """
        if not session_id or not isinstance(session_id, str): # type: ignore
            return
        session = get_obj(UserSession, session_id)
        if not session:
            return

        if (
            session.created_at + timedelta(seconds=self.session_duration)
        ) < datetime.now():
            
            db = DatabaseOp()
            db.delete(session)
            db.commit()
            return

        return session.user_id
    
    def get_session(self, user: User) -> str | None:
        """
        Return a valid active session ID for the given user.
        """
        if not user.user_session:
            return

        user_session_obj = user.user_session[0]
        if (
            user_session_obj.created_at
            + timedelta(seconds=self.session_duration)
            > datetime.now()
        ):
            return user_session_obj.id
        return
