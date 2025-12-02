#!/usr/env python3

"""

"""


from dotenv import load_dotenv
from flask import abort, request
from typing import cast
import logging
import os

from api.v1.utils.utility import UserDisplineHandler
from api.v1.utils.data_validations import UserLogin, validate_request_data
from models import storage
from models.user import User


logger = logging.getLogger(__name__)
load_dotenv()


class BaseAuth:
    """ """

    def require_auth(self, path: str, excluded_paths: list[str]) -> bool:
        """ """
        if not path or not excluded_paths:
            return True

        if not path.endswith("/"):
            path += "/"

        for excluded in excluded_paths:
            if path.startswith(excluded):
                return False
        return True

    def session_cookie(self) -> str | None:
        """ """
        cookie_name = os.getenv("SESSION_NAME")
        if not cookie_name:
            logger.error("SESSION_NAME environment variable not set")
            return
        return request.cookies.get(cookie_name)

    def current_user(self) -> User | None:
        """ """
        pass


class LoginAuth:
    """ """

    def __init__(self) -> None:
        """
        Initializes the LoginAuth instance and
        verifies the session cookie name.
        """
        self.cookie_name = os.getenv("SESSION_NAME")
        if not self.cookie_name:
            logger.error("SESSION_NAME environment variable not set")
            abort(500)

    def authenticate_user(self, email: str, password: str) -> User:
        """
        Authenticate a user by email and password.
        """
        from api.v1.app import bcrypt

        user = storage.search_email(email)
        if not user:
            abort(404, description="Invalid email")

        if not bcrypt.check_password_hash(  # type: ignore
            user.password, password
        ):
            abort(401, description="wrong password")

        return user

    def create_user_session(self, user: User) -> tuple[str, str]:
        """ """
        from api.v1.app import auth

        session_id = auth.create_session(user.id)
        if not session_id:
            logger.error("No session id set")
            abort(500)

        return cast(str, self.cookie_name), session_id

    def get_user_session(self, user: User) -> tuple[str, str] | None:
        """
        Retrieves an existing session for the given user, if any.
        """
        from api.v1.app import auth

        session_id = auth.get_session(user)
        if not session_id:
            return

        return cast(str, self.cookie_name), session_id

    def ensure_user_is_active(self, user: User):
        """ """
        discpline_handler = UserDisplineHandler()
        if not discpline_handler.active_user(user):
            abort(403, description="account suspended. Try again later!")

    def login_user(self) -> dict[str, str]:
        """
        Handles the full user login process:
            - Validates request data.
            - Authenticates credentials.
            - Reuses or creates a session.
        """
        valid_data = validate_request_data(UserLogin)
        email = valid_data.get("email")
        password = valid_data.get("password")

        if not email:
            abort(400, description="Email required")

        if not password:
            abort(400, description="Password required")

        user = self.authenticate_user(email, password)

        self.ensure_user_is_active(user)
        existing_session = self.get_user_session(user)
        if existing_session:
            cookie, session_id = existing_session
        else:
            cookie, session_id = self.create_user_session(user)

        return {"cookie": cookie, "session_id": session_id, "user_id": user.id}
