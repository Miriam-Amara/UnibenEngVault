#!/usr/bin/env python3

"""
Implements login and logout routes for users.
"""


from dotenv import load_dotenv
from flask import abort, jsonify
import logging
import os

from api.v1.views import app_views
from api.v1.auth.authentication import LoginAuth


load_dotenv()
logger = logging.getLogger(__name__)


@app_views.route(
        "/auth_session/login", strict_slashes=False, methods=["POST"]
)
def login():
    """
    Implements login route.
    """
    login_auth = LoginAuth()
    login_data = login_auth.login_user()
    cookie_name = login_data["cookie"]
    session_id = login_data["session_id"]
    user_id = login_data["user_id"]
    session_duration = int(os.getenv("SESSION_DURATION", 0))

    response = jsonify({"user_id": user_id})
    response.set_cookie(
        key=cookie_name,
        value=session_id,
        max_age=session_duration,
        secure=False,
        httponly=True,
        samesite="Lax",
        path="/",
    )
    return response, 200


@app_views.route(
        "/auth_session/logout", strict_slashes=False, methods=["POST"]
)
def logout():
    """
    Implements logout routes.
    """
    from api.v1.app import auth

    if not auth.destroy_session():
        abort(404)
    return jsonify({}), 200
