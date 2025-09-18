#!/usr/bin/env python3

"""

"""


from dotenv import load_dotenv
from flask import request, abort, jsonify
import logging

from api.v1.views import app_views
from api.v1.auth.auth_service import AuthService
from api.v1.utils import get_request_data
from api.v1.data_validations import DatabaseOp



load_dotenv()
logger = logging.getLogger(__name__)

@app_views.route("/auth_session/login", strict_slashes=False, methods=["POST"])
def login():
    """
    """
    db = DatabaseOp()
    auth_service = AuthService()

    email, password = auth_service.validate_login_request(get_request_data())

    # validate email and password
    user = auth_service.authenticate_user(email, password)
    
    auth_service.ensure_user_is_active(user, db)
    cookie_name, session_id = auth_service.create_user_session(user)

    response = jsonify({"user_id": user.id})
    response.set_cookie(
        key=cookie_name,
        value=session_id,
        max_age=3600,
        secure=True,
        httponly=True
    )
    return response, 200    

@app_views.route("/auth_session/logout", strict_slashes=False, methods=["DELETE"])
def logout():
    """
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200