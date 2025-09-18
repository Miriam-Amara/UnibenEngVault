#!/usr/env python3

"""

"""


from dotenv import load_dotenv
from flask import Request
import logging
import os

from models.user import User


logger = logging.getLogger(__name__)
load_dotenv()


class Auth:
    """
    
    """
    def require_auth(self, path: str | None, excluded_paths: list[str] | None) -> bool:
        """ """
        logger.debug(f"{path}")
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        
        if not path.endswith("/"):
            path += "/"
        logger.debug(f"{path}")
        if path in excluded_paths:
            return False
        return True
    
    def authorization_header(self, request: Request | None=None) -> str | None:
        """ """
        logger.debug(f"{request}")
        logger.debug(f"{type(request)}")
        if request is None:
            return
        auth_header = request.headers.get("Cookie", None)
        logger.debug(f"{auth_header}")
        if not auth_header:
            return
        return auth_header
    
    def session_cookie(self, request: Request | None=None) -> str | None:
        """
        """
        if not request:
            return
        
        cookie_name = os.getenv("SESSION_NAME")
        logger.debug(f"{cookie_name}")
        if not cookie_name:
            return
        logger.debug(f"{request.cookies.get(cookie_name)}")
        return request.cookies.get(cookie_name)

    def current_user(self, request: Request | None=None) -> User | None:
        """ """
        pass
