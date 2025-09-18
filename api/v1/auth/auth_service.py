#!/usr/bin/env python3

"""

"""


from dotenv import load_dotenv
from flask import abort
from typing import Any
import logging
import os

from api.v1.data_validations import DatabaseOp
from api.v1.utils import UserDisplineHandler
from models.user import User


load_dotenv()
logger = logging.getLogger(__name__)


class AuthService:
    """
    """
    def validate_login_request(self, data: dict[str, Any]) -> tuple[str, str]:
        """
        """
        email = data.get("email")
        password = data.get("password")

        if not email:
            abort(400, description="email missing")
        if not password:
            abort(400, description="password missing")
        
        return email.lower(), password

    def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate a user by email and password."""
        from api.v1.app import bcrypt

        user = User.search(email)
        if not user:
            abort(404, description="no user found for this email")
        
        if not bcrypt.check_password_hash(user.password, password): # type: ignore
            abort(401, description="wrong password")
        
        return user

    def ensure_user_is_active(self, user: User, db: DatabaseOp):
        """
        """
        discpline_handler = UserDisplineHandler()
        if not discpline_handler.is_user_active(user, db):
            abort(403, description="account suspended. Try again later!")

    def create_user_session(self, user: User) -> tuple[str, str]:
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        if not session_id:
            logger.error("No session id set")
            abort(500)

        cookie_name = os.getenv("SESSION_NAME")
        if not cookie_name:
            logger.error("cookie env variable is empty")
            abort(500)
        
        return cookie_name, session_id
