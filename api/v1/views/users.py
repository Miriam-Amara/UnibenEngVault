#!/usr/bin/env python3

"""

"""


from flask import g, abort, jsonify
from typing import Any, cast
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils import get_obj
from api.v1.data_validations import ValidateData, DatabaseOp
from models.user import User
from models.admin import Admin
from models.department import Department
from models.level import Level



logger = logging.getLogger(__name__)


@app_views.route("/register", strict_slashes=False, methods=["POST"])
def register_users():
    """
    """
    from api.v1.app import bcrypt

    data_validator = ValidateData()
    validated_data = data_validator.validate_request_data("UserCreate")
    if not validated_data:
        logger.error("Invalid validation class name.")
        abort(500)

    department = get_obj("Department", validated_data["department_id"])
    level = get_obj("Level", validated_data["level_id"])
    if not department:
        abort(404, description="department does not exists.")
    if not level:
        abort(404, description="level does not exist.")
    
    validated_data["password"] = (
        bcrypt
        .generate_password_hash(validated_data["password"]) # type: ignore
        .decode("utf-8")
    )

    validated_data["role"] = validated_data["role"].value
    user = User(**validated_data)
    db = DatabaseOp()
    db.save(user)

    if validated_data["role"] == "admin":
        admin = Admin()
        user.admin = admin
        db.save(user)
    user_dict = user.to_dict()
    logger.debug(f"{user_dict}")
    user_dict.pop("admin", None)
    logger.debug(f"{user_dict}")
    return jsonify(user_dict), 201

# allow only admins
@app_views.route(
        "/admins/users/<department_id>/<level_id>/<int:page_size>/<int:page_num>",
        strict_slashes=False, methods=["GET"]
    )
@admin_only
def get_users_by_department_and_level(
    department_id: str, level_id:str,
    page_size: int, page_num: int
):
    """
    """
    department = cast(Department, get_obj("Department", department_id))
    level = cast(Level, get_obj("Level", level_id))
    if not department:
        abort(404, description="department does not exist.")
    if not level:
        abort(404, description="level does not exist")

    users = cast(list[User], User.get_users_by_deparment_and_level(
        department.id, level.id, page_size, page_num)
    )
    if not users:
        abort(404, description="no user found for the department and level.")
    
    users_dicts: list[dict[str, Any]] = [user.to_dict() for user in users]
    return jsonify(users_dicts), 200

@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def get_user(user_id: str):
    """
    """
    if user_id == "me" and g.current_user == None:
        abort(404)
    
    if user_id == "me" and g.current_user:
        user = g.current_user
    else:
        user = get_obj("User", user_id)
        if not user:
            abort(404)
    
    authenticated_user = user.to_dict()
    return jsonify(authenticated_user), 200

@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id: str):
    """
    """
    data_validator = ValidateData()
    validated_data = data_validator.validate_request_data("UserUpdate")
    if not validated_data:
        logger.error("Invalid validation class name.")
        abort(500)

    user = cast(User, get_obj("User", user_id))
    if not user:
        abort(404, description="user does not exist.")
    
    for attr, value in validated_data.items():
        setattr(user, attr, value)
    db = DatabaseOp()
    db.save(user)

    logger.debug(f"{user.role}")
    if user.role.value == "admin":
        admin = Admin(user_id=user.id)
        db.save(admin)
    
    user_dict = user.to_dict()
    logger.debug(f"{user_dict}")
    return jsonify(user_dict), 200

# allow only admins
@app_views.route("/admins/users/<user_id>", strict_slashes=False, methods=["DELETE"])
@admin_only
def delete_user(user_id: str):
    """
    """
    user = cast(User, get_obj("User", user_id))
    if not user:
        abort(404)
    
    db = DatabaseOp()
    db.delete(user)
    db.commit()
    return jsonify({}), 200
