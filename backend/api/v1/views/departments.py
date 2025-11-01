#!/usr/bin/env python3

"""

"""


from flask import abort, jsonify
from typing import Any
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils.utility import get_obj, DatabaseOp
from api.v1.utils.data_validations import (
    validate_request_data, DepartmentCreate, DepartmentUpdate
)
from models import storage
from models.department import Department


logger = logging.getLogger(__name__)


def get_department_dict(department: Department) -> dict[str, Any]:
    """
    """
    dept_dict = department.to_dict()
    dept_dict.pop("__class__", None)
    dept_dict["courses"] = len(department.courses)
    
    count_100level = 0
    count_200level = 0
    count_300level = 0
    count_400level = 0
    count_500level = 0
    for course in department.courses:
        if course.level.name == 100:
            count_100level += 1
        elif course.level.name == 200:
            count_200level += 1
        elif course.level.name == 300:
            count_300level += 1
        elif course.level.name == 400:
            count_400level += 1
        elif course.level.name == 500:
            count_500level += 1
    
    dept_level_courses_count = {
        "level_100": count_100level,
        "level_200": count_200level,
        "level_300": count_300level,
        "level_400": count_400level,
        "level_500": count_500level
    }
    dept_dict["dept_level_courses_count"] = dept_level_courses_count
    return dept_dict


@app_views.route(
        "/departments",
        strict_slashes=False,
        methods=["POST"]
    )
@admin_only
def create_department():
    """
    """
    valid_data = validate_request_data(DepartmentCreate)

    department = Department(**valid_data)
    db = DatabaseOp()
    db.save(department)

    dept_dict = get_department_dict(department)
    return jsonify(dept_dict), 201


@app_views.route(
        "/departments/<int:page_size>/<int:page_num>",
        strict_slashes=False,
        methods=["GET"]
    )
def get_all_departments(page_size: int, page_num: int):
    """
    """
    departments = storage.all(Department, page_size, page_num)
    if not departments:
        abort(404, description="No department found")
    all_departments = [
        get_department_dict(dept) for dept in departments
    ]
    return jsonify(all_departments), 200


@app_views.route(
        "/departments/<dept_id>",
        strict_slashes=False,
        methods=["GET"]
    )
def get_department(dept_id: str):
    """
    """
    department = get_obj(Department, dept_id)
    if not department:
        abort(404, description=f"Department does not exist")

    dept_dict = get_department_dict(department)
    return jsonify(dept_dict), 200


@app_views.route(
        "/departments/<dept_id>",
        strict_slashes=False,
        methods=["PUT"]
    )
@admin_only
def update_department(dept_id: str):
    """
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
        "/departments/<dept_id>",
        strict_slashes=False,
        methods=["DELETE"]
    )
@admin_only
def delete_department(dept_id: str):
    """
    """
    department = get_obj(Department, dept_id)
    if not department:
        abort(404, description="Department does not exist.")
    
    db = DatabaseOp()
    db.delete(department)
    db.commit()
    return jsonify({}), 200
