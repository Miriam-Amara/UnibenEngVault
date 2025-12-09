#!/usr/bin/env python3

"""
Implements routes for CRUD (Create, Read, Update and Delete)
operations on departments.
"""


from flask import abort, jsonify, request
from typing import Any
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils.utility import get_obj, DatabaseOp
from api.v1.utils.data_validations import (
    validate_request_data,
    DepartmentCreate,
    DepartmentUpdate,
)
from models import storage
from models.department import Department


logger = logging.getLogger(__name__)


def get_department_dict(department: Department) -> dict[str, Any]:
    """
    Return a json serializable dict of the department object.
    """
    num_of_users_in_dept: int = len(department.users)
    num_of_courses_offered: int = len(department.courses)

    dept_dict = department.to_dict()
    dept_dict["num_of_users"] = num_of_users_in_dept
    dept_dict["num_of_courses"] = num_of_courses_offered
    dept_dict.pop("courses", None)
    dept_dict.pop("users", None)
    dept_dict.pop("__class__", None)
    return dept_dict


@app_views.route(
        "/departments", strict_slashes=False, methods=["POST"]
)
@admin_only
def create_department():
    """
    Implements route for creating and adding
    new departments to the database.
    """
    valid_data = validate_request_data(DepartmentCreate)

    department = Department(**valid_data)
    db = DatabaseOp()
    db.save(department)

    dept_dict = get_department_dict(department)
    return jsonify(dept_dict), 201


@app_views.route("/departments", strict_slashes=False, methods=["GET"])
def get_all_departments():
    """
    Retrieves all departments with optional
    filtering by date and pagination.
    """
    page_size: str | None = request.args.get("page_size")
    page_num: str | None = request.args.get("page_num")
    created_at: str | None = request.args.get("date")
    dept_name: str | None = request.args.get("search")

    if dept_name or created_at:
        departments = storage.filter(
            Department,
            search_str=dept_name,
            date_str=created_at,
            page_size=page_size,
            page_num=page_num,
        )
    else:
        departments = storage.all(
            Department,
            page_size=page_size,
            page_num=page_num
        )
    if not departments:
        abort(404, description="No department found")
    all_departments = [get_department_dict(dept) for dept in departments]
    return jsonify(all_departments), 200


@app_views.route(
        "/departments/<dept_id>", strict_slashes=False, methods=["GET"]
)
def get_department(dept_id: str):
    """
    Retrieves a department from the database by its id.
    """
    department = get_obj(Department, dept_id)
    if not department:
        abort(404, description=f"Department does not exist")

    dept_dict = get_department_dict(department)
    return jsonify(dept_dict), 200


@app_views.route(
        "/departments/<dept_id>", strict_slashes=False, methods=["PUT"]
)
@admin_only
def update_department(dept_id: str):
    """
    Update a department details and save to the database.
    """
    valid_data = validate_request_data(DepartmentUpdate)

    department = get_obj(Department, dept_id)
    if not department:
        abort(404, description="Department does not exist.")

    for attr, value in valid_data.items():
        setattr(department, attr, value)

    db = DatabaseOp()
    db.save(department)

    dept_dict = get_department_dict(department)
    return jsonify(dept_dict), 200


@app_views.route(
        "/departments/<dept_id>", strict_slashes=False, methods=["DELETE"]
)
@admin_only
def delete_department(dept_id: str):
    """
    Delete a department from the database using its id.
    """
    department = get_obj(Department, dept_id)
    if not department:
        abort(404, description="Department does not exist.")

    db = DatabaseOp()
    db.delete(department)
    db.commit()
    return jsonify({}), 200
