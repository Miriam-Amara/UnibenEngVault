#!/usr/bin/env python3

"""

"""


from flask import g, abort, jsonify
from typing import Optional, cast
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils import get_obj, UserDisplineHandler
from api.v1.data_validations import ValidateData, DatabaseOp
from models import storage
from models.user import User, UserWarning


logger = logging.getLogger(__name__)


# allow only admins
@app_views.route("/admins/users/<user_id>/warnings", methods=["POST"])
@admin_only
def issue_user_warning(user_id: str):
    """
    """
    admin = g.current_user.admin
    discipline_handler = UserDisplineHandler()

    data_validator = ValidateData()
    validated_data = data_validator.validate_request_data("UserWarningCreate")
    if not validated_data:
        logger.error(f"Invalid validation class name")
        abort(500)

    reason = validated_data["reason"]
    logger.debug(f"{reason}")

    user = cast(User, get_obj("User", user_id))
    if not user:
        abort(404, description="user not found")

    db = DatabaseOp()
    warning = discipline_handler.create_user_warning(user, admin, reason, db)
    discipline_handler.handle_suspension(user, db)
    discipline_handler.handle_termination(user, db)

    return jsonify(warning.to_dict()), 201

# allow only admins
@app_views.route("/admins/users/warnings/<int:page_size>/<int:page_num>", methods=["GET"])
@admin_only
def all_user_warnings(page_size: int, page_num: int):
    """
    """
    user_warnings: Optional[list[UserWarning]] = storage.all(page_size, page_num, "UserWarning")
    if not user_warnings:
        abort(404, description="no user warning found")
    
    user_warning_dicts = [warning.to_dict(include_relationships=True) for warning in user_warnings]
    logger.debug(f"{user_warning_dicts}")
    return jsonify(user_warning_dicts), 200


# allow only admins
@app_views.route("/admins/users/<user_id>/warnings", methods=["GET"])
@admin_only
def get_user_warnings(user_id: str):
    """
    """
    user = cast(User, get_obj("User", user_id))
    if not user:
        abort(404, description="user does not exist.")
    
    user_warnings = [warning.to_dict() for warning in user.warnings]
    return jsonify(user_warnings), 200

# allow only admins
@app_views.route("/admins/users/warnings/<user_warning_id>", methods=["PUT"])
@admin_only
def edit_user_warnings(user_warning_id: str):
    """
    """
    data_validator = ValidateData()
    validated_data = data_validator.validate_request_data("UserWarningUpdate")
    if not validated_data:
        logger.error(f"Invalid validation class name")
        abort(500)

    user_warning = cast(UserWarning, get_obj("UserWarning", user_warning_id))
    if not user_warning:
        abort(404, description="user warning does not exist.")
    
    for attr, value in validated_data:
        setattr(user_warning, attr, value)
    
    db = DatabaseOp()
    db.save(user_warning)
    return jsonify(user_warning.to_dict()), 200

# allow only admins
@app_views.route("/admins/users/warnings/<user_warning_id>", methods=["DELETE"])
@admin_only
def delete_user_warnings(user_warning_id: str):
    """
    """
    user_warning = cast(UserWarning, get_obj("UserWarning", user_warning_id))
    if not user_warning:
        abort(404, description="user warning does not exist.")
    
    user_warning.issued_to.warnings_count -= 1
    db = DatabaseOp()
    db.delete(user_warning)
    db.commit()

    return jsonify({}), 200
