#!/usr/bin/env python3

"""

"""


from flask import g, abort, jsonify
from typing import Sequence
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils.utility import get_obj, DatabaseOp, UserDisplineHandler
from api.v1.utils.data_validations import (
    validate_request_data, UserWarningCreate, UserWarningUpdate
)
from models import storage
from models.user import User, UserWarning


logger = logging.getLogger(__name__)


# allow only admins
@app_views.route("/users/<user_id>/warnings", methods=["POST"])
@admin_only
def issue_user_warning(user_id: str):
    """
    """
    admin = g.current_user.admin
    valid_data = validate_request_data(UserWarningCreate)

    user = get_obj(User, user_id)
    if not user:
        abort(404, description="User not found.")

    discipline_handler = UserDisplineHandler()
    warning = discipline_handler.create_user_warning(
        user, admin, valid_data["reason"]
    )
    discipline_handler.handle_suspension(user)
    discipline_handler.handle_termination(user)

    return jsonify(warning.to_dict()), 201


# allow only admins
@app_views.route(
        "/users/warnings/<int:page_size>/<int:page_num>",
        strict_slashes=False,
        methods=["GET"]
    )
@admin_only
def all_user_warnings(page_size: int, page_num: int):
    """
    """
    user_warnings: Sequence[UserWarning] = storage.all(
        UserWarning,page_size, page_num
    )
    if not user_warnings:
        abort(404, description="No user warning found")
    
    user_warning_dicts = [warning.to_dict() for warning in user_warnings]
    return jsonify(user_warning_dicts), 200


# allow only admins
@app_views.route(
        "/users/<user_id>/warnings",
        strict_slashes=False,
        methods=["GET"]
    )
@admin_only
def get_user_warnings(user_id: str):
    """
    """
    user = get_obj(User, user_id)
    if not user:
        abort(404, description="User does not exist.")
    
    user_warnings = [warning.to_dict() for warning in user.warnings]
    return jsonify(user_warnings), 200


# allow only admins
@app_views.route(
        "/users/warnings/<user_warning_id>",
        strict_slashes=False,
        methods=["PUT"]
    )
@admin_only
def update_user_warnings(user_warning_id: str):
    """
    """
    valid_data = validate_request_data(UserWarningUpdate)

    if "user_id" in valid_data:
        user = get_obj(User, valid_data["user_id"])
        if not user:
            abort(404, description="User does not exist.")

    user_warning = get_obj(UserWarning, user_warning_id)
    if not user_warning:
        abort(404, description="User warning does not exist.")
    
    for attr, value in valid_data:
        setattr(user_warning, attr, value)
    
    db = DatabaseOp()
    db.save(user_warning)
    return jsonify(user_warning.to_dict()), 200

# allow only admins
@app_views.route(
        "/users/warnings/<user_warning_id>",
        strict_slashes=False,
        methods=["DELETE"]
    )
@admin_only
def delete_user_warnings(user_warning_id: str):
    """
    """
    user_warning = get_obj(UserWarning, user_warning_id)
    if not user_warning:
        abort(404, description="User warning does not exist.")
    
    user_warning.issued_to.warnings_count -= 1
    db = DatabaseOp()
    db.delete(user_warning)
    db.commit()

    return jsonify({}), 200
