#!/usr/bin/env python3

"""
Implements routes for CRUD (Create, Read, Update and Delete)
operations on courses.
"""


from flask import g, abort, jsonify, request
from typing import Any, cast
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils.utility import get_obj, DatabaseOp
from api.v1.utils.data_validations import (
    validate_request_data,
    CourseCreate,
    CourseUpdate,
)
from models import storage
from models.admin import Admin
from models.course import Course
from models.level import Level


logger = logging.getLogger(__name__)


def get_course_dict(course: Course) -> dict[str, Any]:
    """
    Returns a json serializable dict of the course object.
    """
    course_dict = course.to_dict()
    course_dict["course_code"] = course_dict["course_code"].upper()
    course_dict["level"] = course.level.level_name
    course_dict["num_of_files_in_course"] = len(course.files)
    course_dict["departments"] = [
        department.dept_name for department in course.departments
    ]
    course_dict["added_by"] = course.added_by.user.email
    course_dict.pop("files", None)
    course_dict.pop("__class__", None)

    return course_dict


@app_views.route("/courses", strict_slashes=False, methods=["POST"])
@admin_only
def add_course():
    """
    Create and add a course to the database
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


@app_views.route("/courses", strict_slashes=False, methods=["GET"])
@admin_only
def get_all_courses():
    """
    Returns all courses in the database with optional filtering by:
    date, search and pagination.
    """
    page_size: str | None = request.args.get("page_size")
    page_num: str | None = request.args.get("page_num")
    created_at: str | None = request.args.get("date")
    course_code: str | None = request.args.get("search")

    if course_code or created_at:
        courses = storage.filter(
            Course,
            search_str=course_code,
            date_str=created_at,
            page_size=page_size,
            page_num=page_num,
        )
    else:
        courses = storage.all(
            Course,
            page_size=page_size,
            page_num=page_num,
        )

    if not Course:
        abort(404, description="No course found")
    all_courses = [get_course_dict(course) for course in courses]
    return jsonify(all_courses), 200


@app_views.route(
        "/courses/<course_id>", strict_slashes=False, methods=["GET"]
)
@admin_only
def get_course(course_id: str):
    """
    Return a course details given its id.
    """
    course = get_obj(Course, course_id)
    if not course:
        abort(404, description="Course does not exist.")

    course_dict = get_course_dict(course)
    return jsonify(course_dict), 200


@app_views.route(
        "/courses/<course_id>", strict_slashes=False, methods=["PUT"]
)
@admin_only
def update_course(course_id: str):
    """
    Update the details of a course using its id.
    """
    valid_data = validate_request_data(CourseUpdate)

    if "level_id" in valid_data:
        level = get_obj(Level, valid_data["level_id"])
        if not level:
            abort(404, description="Level does not exist.")

    course = get_obj(Course, course_id)
    if not course:
        abort(404, description="Course does not exist.")

    for attr, value in valid_data.items():
        setattr(course, attr, value)

    db = DatabaseOp()
    db.save(course)

    course_dict = get_course_dict(course)
    return jsonify(course_dict), 200


@app_views.route(
        "/courses/<course_id>", strict_slashes=False, methods=["DELETE"]
)
@admin_only
def delete_course(course_id: str):
    """
    Deletes a course from the database.
    """
    course = get_obj(Course, course_id)
    if not course:
        abort(404, description="course does not exist.")

    db = DatabaseOp()
    db.delete(course)
    db.commit()
    return jsonify({}), 200
