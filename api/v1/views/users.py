#!/usr/bin/env python3

"""

"""


from flask import abort, jsonify
from typing import Any, cast
import logging

from api.v1.views import app_views
from api.v1.utils import get_obj
from api.v1.data_validations import ValidateData, DatabaseOp
from models.user import User
from models.department import Department
from models.level import Level



logger = logging.getLogger(__name__)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
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
    if not department or not level:
        abort(404)
    
    validated_data["password"] = (
        bcrypt
        .generate_password_hash(validated_data["password"]) # type: ignore
        .decode("utf-8")
    )
    logger.debug(f"{validated_data}")
    validated_data["role"] = validated_data["role"].value
    user = User(**validated_data)

    db = DatabaseOp()
    db.save(user)
    return user.to_dict(), 201

# allow only admins
@app_views.route(
        "/admin/users/<department_id>/<level_id>/<int:page_size>/<int:page_num>",
        strict_slashes=False, methods=["GET"]
    )
def get_users_by_department_and_level(
    department_id: str, level_id:str,
    page_size: int, page_num: int
):
    """
    """
    department = cast(Department, get_obj("Department", department_id))
    level = cast(Level, get_obj("Level", level_id))
    if not department or not level:
        abort(404)

    user_objects = cast(list[User], User.get_users_by_deparment_and_level(
        department.id, level.id, page_size, page_num)
    )
    if not user_objects:
        abort(404)
    
    users: list[dict[str, Any]] = []
    for user in user_objects:
        user_data = user.to_dict()
        user_data["role"] = user_data["role"].value
        users.append(user_data)
    return users, 200

@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def get_user(user_id: str):
    """
    """
    user = get_obj("User", user_id)
    if not user:
        abort(404)
    
    user_data = user.to_dict()
    user_data["role"] = user_data["role"].value
    return user_data, 200

@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id: str):
    """
    """
    data_validator = ValidateData()
    validated_data = data_validator.validate_request_data("UserUpdate")
    if not validated_data:
        logger.error("Invalid validation class name.")
        abort(500)
    
    if validated_data.get("role"):
        validated_data["role"] = validated_data["role"].value
    logger.debug(f"{validated_data}")
    user = cast(User, get_obj("User", user_id))
    if not user:
        abort(404)
    
    for attr, value in validated_data.items():
        setattr(user, attr, value)
    db = DatabaseOp()
    db.save(user)
    user_data = user.to_dict()
    user_data["role"] = user_data["role"].value
    return user_data, 200

# allow only admins
@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def delete_user(user_id: str):
    """
    """
    user = cast(User, get_obj("User", user_id))
    if not user:
        abort(404)
    
    db = DatabaseOp()
    db.delete(user)
    db.save(user)
    return jsonify({}), 200
