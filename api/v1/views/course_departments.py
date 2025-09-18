#!/usr/bin/env python3

"""

"""


from flask import request, abort, jsonify
from typing import cast
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils import get_obj
from api.v1.data_validations import DatabaseOp
from models import storage
from models.course import Course
from models.department import Department


logger = logging.getLogger(__name__)


# allow only admins
@app_views.route("/admins/courses/<course_id>/departments/<department_id>", methods=["POST"])
@admin_only
def add_course_departments(course_id: str, department_id: str):
    """
    """
    course = cast(Course, get_obj("Course", course_id))
    department = get_obj("Department", department_id)
    if not course:
        abort(404, description="course does not exist.")
    if not department:
        abort(404, description="department does not exist.")
    
    db = DatabaseOp()
    course.departments.append(department)
    db.save(course)

    course_dict = course.to_dict()
    course_dict.pop("level", None)
    course_dict.pop("registered_by", None)
    course_dict.pop("files", None)
    
    logger.debug(f"{course_dict}")
    return jsonify(course_dict), 201

# allow only admins
@app_views.route("/admins/departments/<department_id>/courses/<course_id>", methods=["POST"])
@admin_only
def add_department_courses(department_id: str, course_id: str):
    """
    """
    department = cast(Department, get_obj("Department", department_id))
    course = get_obj("Course", course_id)
    if not department:
        abort(404, description="department does not exist.")  
    if not course:
        abort(404, description="course does not exist.")
    
    db = DatabaseOp()
    department.courses.append(course)
    db.save(department)

    dept_dict = department.to_dict(include_relationships=True)
    dept_dict.pop("users", None)
    dept_dict.pop("admin_permissions", None)
    logger.debug(f"{dept_dict}")
    
    return jsonify(dept_dict), 201

@app_views.route("/courses/<course_id>/departments", methods=["GET"])
def get_course_departments(course_id: str):
    """
    """
    course = cast(Course, get_obj("Course", course_id))
    if not course:
        abort(404, description="course does not exist.")
    
    course_departments = [department.to_dict() for department in course.departments]
    logger.debug(f"{course_departments}")
    return jsonify(course_departments), 200

@app_views.route("/departments/<department_id>/levels/<level_id>/courses", methods=["GET"])
def get_courses_by_department_and_level(department_id: str, level_id: str):
    """
    """
    semester = request.args.get("semester")
    if semester and semester.lower().strip() not in ["first", "second"]:
        semester = None
    
    department = get_obj("Department", department_id)
    level = get_obj("Level", level_id)
    if not department:
        abort(404, description="department does not exist.")
    if not level:
        abort(404, description="level does not exist.")
    
    department_level_courses_objects = storage.get_courses_by_department_and_level(
        department_id, level_id, semester=semester
    )
    if not department_level_courses_objects:
        abort(404, description="no courses found for the department.")
    all_department_level_courses = [
        course.to_dict() for course in department_level_courses_objects
    ]
    logger.debug(f"{all_department_level_courses}")
    return jsonify(all_department_level_courses), 200


# allow only admins
@app_views.route("/admins/courses/<course_id>/departments/<department_id>", methods=["DELETE"])
@admin_only
def delete_course_department(course_id: str, department_id: str):
    """
    """
    course = cast(Course, get_obj("Course", course_id))
    department = get_obj("Department", department_id)
    if not course:
        abort(404, description="course does not exist.")
    if not department:
        abort(404, description="department does not exist.")

    course.departments.remove(department)
    db = DatabaseOp()
    db.save(course)
    return jsonify({}), 200    
