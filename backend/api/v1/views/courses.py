#!/usr/bin/env python3

"""

"""


from flask import g, abort, jsonify
from typing import Any, cast
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils.utility import get_obj, DatabaseOp
from api.v1.utils.data_validations import (
    validate_request_data, CourseCreate, CourseUpdate
)
from models import storage
from models.admin import Admin
from models.course import Course
from models.level import Level


logger = logging.getLogger(__name__)


def get_course_dict(course: Course) -> dict[str, Any]:
    """
    """
    course_dict = course.to_dict()
    course_dict["level"] = course.level.name
    course_dict["files"] = len(course.files)
    course_dict["departments"] = [
        department.dept_code for department in course.departments
    ]
    return course_dict


# allow only admins
@app_views.route(
        "/courses", strict_slashes=False, methods=["POST"]
    )
@admin_only
def add_course():
    """
    """
    admin = cast(Admin, g.current_user.admin)

    valid_data = validate_request_data(CourseCreate)

    level = get_obj(Level, valid_data["level_id"])
    if not level:
        abort(404, description="Level does not exist")
    
    valid_data["admin_id"] = admin.id
    valid_data["level_id"] = level.id

    db = DatabaseOp()
    course = Course(**valid_data)
    db.save(course)

    course_dict = get_course_dict(course)
    return jsonify(course_dict), 201


# allow only admins
@app_views.route(
        "/courses/<int:page_size>/<int:page_num>",
        strict_slashes=False,
        methods=["GET"]
    )
@admin_only
def get_all_courses(page_size: int, page_num: int):
    """
    """
    courses = storage.all(Course, page_size, page_num)
    if not Course:
        abort(404, description="No course found")
    all_courses = [
        get_course_dict(course) for course in courses
    ]
    return jsonify(all_courses), 200


# allow only admins
@app_views.route(
        "/courses/<course_id>", methods=["GET"]
    )
@admin_only
def get_course(course_id: str):
    """
    """
    course = get_obj(Course, course_id)
    if not course:
        abort(404, description="Course does not exist.")

    course_dict = get_course_dict(course)
    return jsonify(course_dict), 200


# allow only admins
@app_views.route("/courses/<course_id>", methods=["PUT"])
@admin_only
def update_course(course_id: str):
    """
    """
    valid_data = validate_request_data(CourseUpdate)
    
    if "level_id" in valid_data:
        level = get_obj(Level, valid_data["level_id"])
        if not level:
            abort(404, description="Level does not exist.")

    course = get_obj(Course, course_id)
    if not course:
        abort(404, description="course does not exist.")
    
    for attr, value in valid_data.items():
        setattr(course, attr, value)
    
    db = DatabaseOp()
    db.save(course)
    
    course_dict = get_course_dict(course)
    return jsonify(course_dict), 200


# allow only admins
@app_views.route("/courses/<course_id>", methods=["DELETE"])
@admin_only
def delete_course(course_id: str):
    """
    """
    course = get_obj(Course, course_id)
    if not course:
        abort(404, description="course does not exist.")

    db = DatabaseOp()
    db.delete(course)
    db.commit()
    return jsonify({}), 200
