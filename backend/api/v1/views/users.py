#!/usr/bin/env python3

"""
Implements routes for CRUD (Create, Read, Update and Delete)
operations on users.
"""


from flask import g, abort, jsonify, request
from typing import Any, Sequence
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils.utility import get_obj, DatabaseOp
from api.v1.utils.data_validations import (
    UserCreate, UserUpdate, validate_request_data
)
from models import storage
from models.user import User
from models.admin import Admin
from models.department import Department
from models.level import Level


logger = logging.getLogger(__name__)


def get_user_dict(user: User) -> dict[str, Any]:
    """
    Returns a json serializable dict for the given user object.
    """
    user_dict = user.to_dict()
    user_dict.pop("__User__", None)

    if user.department:
        user_dict["department"] = user.department.dept_code.upper()
    if user.level:
        user_dict["level"] = user.level.level_name
    user_dict["course_files_added"] = len(user.course_files_added)
    user_dict["tutorial_links_added"] = len(user.tutorial_links_added)
    user_dict["feedbacks_added"] = len(user.feedbacks_added)
    user_dict["helps_added"] = len(user.helps_added)
    user_dict["reports_added"] = len(user.reports_added)
    return user_dict


@app_views.route("/register", strict_slashes=False, methods=["POST"])
def register_users():
    """
    Implements route for registering users.
    """
    from api.v1.app import bcrypt

    valid_data = validate_request_data(UserCreate)

    if "department_id" in valid_data:
        department = get_obj(Department, valid_data["department_id"])
        if not department:
            abort(404, description="Department does not exist.")

    if "level_id" in valid_data:
        level = get_obj(Level, valid_data["level_id"])
        if not level:
            abort(404, description="Level does not exist.")

    valid_data["password"] = (
        bcrypt.generate_password_hash(valid_data["password"])  # type: ignore
        .decode("utf-8")
    )

    user = User(**valid_data)

    db = DatabaseOp()
    db.save(user)
    if user.is_admin:
        admin = Admin(user_id=user.id)
        db.save(admin)

    user_dict = get_user_dict(user)
    return jsonify(user_dict), 201


@app_views.route("/users", strict_slashes=False, methods=["GET"])
def get_all_users():
    """
    Returns all users in storage optionally filtered by
    creation date, email and pagination.
    """
    page_size: str | None = request.args.get("page_size")
    page_num: str | None = request.args.get("page_num")
    created_at: str | None = request.args.get("created_at")
    email_str: str | None = request.args.get("search")

    if email_str or created_at:
        users = storage.filter(
            User,
            search_str=email_str,
            date_str=created_at,
            page_size=page_size,
            page_num=page_num,
        )
    else:
        users = storage.all(
            User,
            page_size=page_size,
            page_num=page_num,
        )

    if not users:
        abort(404, description="No user found.")

    all_users = [get_user_dict(user) for user in users]
    return jsonify(all_users), 200


@app_views.route(
    "/users/<department_id>/<level_id>",
    strict_slashes=False,
    methods=["GET"],
)
@admin_only
def get_users_by_department_and_level(
    department_id: str, level_id: str,
):
    """
    Returns all users in a specific department and level.
    """
    page_size = request.args.get("page_size")
    page_num = request.args.get("page_num")

    department = get_obj(Department, department_id)
    if not department:
        abort(404, description="Department does not exist.")

    level = get_obj(Level, level_id)
    if not level:
        abort(404, description="Level does not exist.")

    users: Sequence[User] | None = storage.get_users_by_dept_and_level(
        department.id,
        level.id,
        page_size=page_size,
        page_num=page_num
    )

    if not users:
        abort(
            404,
            description="Users not found for the department and level."
        )

    users_list: list[dict[str, Any]] = [
        get_user_dict(user) for user in users
    ]
    return jsonify(users_list), 200


@app_views.route(
        "/users/<user_id>", strict_slashes=False, methods=["GET"]
)
def get_user(user_id: str):
    """
    Returns a user by id or "me"
    """
    if user_id == "me":
        user = g.current_user
    else:
        user = get_obj(User, user_id)
        if not user:
            abort(404, description="User does not exist")

    user_dict = get_user_dict(user)
    return jsonify(user_dict), 200


@app_views.route(
        "/users/<user_id>", strict_slashes=False, methods=["PUT"]
)
def update_user(user_id: str):
    """
    Updates user details in the database.
    """
    valid_data = validate_request_data(UserUpdate)

    if "department_id" in valid_data:
        department = get_obj(Department, valid_data["department_id"])
        if not department:
            abort(404, description="Department does not exist.")

    if "level_id" in valid_data:
        level = get_obj(Level, valid_data["level_id"])
        if not level:
            abort(404, description="Level does not exist.")

    user = get_obj(User, user_id)
    if not user:
        abort(404, description="User does not exist.")

    for attr, value in valid_data.items():
        setattr(user, attr, value)
    db = DatabaseOp()
    db.save(user)

    if user.is_admin and not user.admin:
        admin = Admin(user_id=user.id)
        db.save(admin)

    user_dict = get_user_dict(user)
    user_dict.pop("admin", None)
    return jsonify(user_dict), 200


@app_views.route(
        "/users/<user_id>", strict_slashes=False, methods=["DELETE"]
)
@admin_only
def delete_user(user_id: str):
    """
    Deletes a user from the database.
    """
    user = get_obj(User, user_id)
    if not user:
        abort(404, description="User does not exist.")

    db = DatabaseOp()
    db.delete(user)
    db.commit()
    return jsonify({}), 200
