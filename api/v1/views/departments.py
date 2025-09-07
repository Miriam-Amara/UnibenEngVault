#!/usr/bin/env python3

"""

"""


from flask import abort, jsonify
from typing import cast
import logging

from api.v1.views import app_views
from api.v1.utils import get_obj
from api.v1.data_validations import ValidateData, DatabaseOp
from models import storage
from models.department import Department


logger = logging.getLogger(__name__)


# allow only admins
@app_views.route("/admin/departments", strict_slashes=False, methods=["POST"])
def create_department():
    """
    """
    data_validator = ValidateData()
    validated_data = data_validator.validate_request_data("DepartmentCreate")

    if not validated_data:
        logger.debug(f"Invalid validation class name")
        abort(500)

    department = Department(**validated_data)
    db = DatabaseOp()
    db.save(department)
    return department.to_dict(), 201


@app_views.route("/departments/<int:page_size>/<int:page_num>", strict_slashes=False, methods=["GET"])
def get_departments(page_size: int, page_num: int):
    """
    """
    dept_objects = storage.all(page_size, page_num, "Department")
    if not dept_objects:
        abort(404)
    all_departments = [dept_obj.to_dict() for dept_obj in dept_objects]
    return all_departments, 200


@app_views.route("/departments/<dept_id>", strict_slashes=False, methods=["GET"])
def get_department(dept_id: str):
    """
    """
    department: Department = cast(Department, get_obj("Department", dept_id))
    if not department:
        abort(404)
    return department.to_dict(), 200

# allow only admins
@app_views.route("/admin/departments/<dept_id>", strict_slashes=False, methods=["PUT"])
def update_department(dept_id: str):
    """
    """
    data_validator = ValidateData()
    validated_data = data_validator.validate_request_data("DepartmentUpdate")
    if not validated_data:
        logger.debug(f"Invalid validation class name")
        abort(500)
    
    department: Department = cast(Department, get_obj("Department", dept_id))
    if not department:
        abort(404)
    
    for attr, value in validated_data.items():
        setattr(department, attr, value)

    db = DatabaseOp()
    db.save(department)
    return department.to_dict(), 200

# allow only admins
@app_views.route("/admin/departments/<dept_id>", strict_slashes=False, methods=["DELETE"])
def delete_department(dept_id: str):
    """
    """
    department = cast(Department, get_obj("Department", dept_id))
    if not department:
        abort(404)
    
    db = DatabaseOp()
    db.delete(department)
    db.save(department)
    return jsonify({}), 200
