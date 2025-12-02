#!/usr/bin/env python3

"""
Implements routes for CRUD (Create, Read, Update and Delete)
operations on combination of courses and departments.
"""


from flask import abort, jsonify, request
from typing import Any
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils.utility import get_obj, DatabaseOp
from models import storage
from models.course import Course
from models.department import Department
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


@app_views.route(
    "/courses/<course_id>/departments/<department_id>",
    strict_slashes=False,
    methods=["POST"],
)
@admin_only
def add_department_to_course(course_id: str, department_id: str):
    """
    Adds a department to a course.
    """
    course = get_obj(Course, course_id)
    if not course:
        abort(404, description="Course does not exist.")

    department = get_obj(Department, department_id)
    if not department:
        abort(404, description="Department does not exist.")

    if department not in course.departments:
        course.departments.append(department)
        db = DatabaseOp()
        db.save(course)

    course_dict = get_course_dict(course)
    return jsonify(course_dict), 201


@app_views.route(
    "/departments/<department_id>/courses/<course_id>",
    strict_slashes=False,
    methods=["POST"],
)
@admin_only
def add_course_to_department(department_id: str, course_id: str):
    """
    Adds a course to a department
    """
    department = get_obj(Department, department_id)
    if not department:
        abort(404, description="Department does not exist.")

    course = get_obj(Course, course_id)
    if not course:
        abort(404, description="Course does not exist.")

    if course not in department.courses:
        department.courses.append(course)
        db = DatabaseOp()
        db.save(department)

    dept_dict = get_course_dict(course)
    return jsonify(dept_dict), 201


@app_views.route(
    "/departments/<department_id>/levels/<level_id>/courses",
    strict_slashes=False,
    methods=["GET"],
)
def get_courses_by_department_and_level(department_id: str, level_id: str):
    """
    Retrieves all courses offered by a specific department and level and
    optionally filter by semester.
    """
    semester: str | None = request.args.get("semester")

    department = get_obj(Department, department_id)
    if not department:
        abort(404, description="Department does not exist.")

    level = get_obj(Level, level_id)
    if not level:
        abort(404, description="Level does not exist.")

    courses = storage.get_courses_by_dept_and_level(
        department.id, level.id, semester=semester
    )

    if not courses:
        abort(
            404,
            description="No course found for the department and level."
        )

    courses_dict: list[dict[str, Any]] = [
        get_course_dict(course) for course in courses
    ]

    return jsonify(courses_dict), 200


@app_views.route(
    "/courses/<course_id>/departments/<department_id>",
    strict_slashes=False,
    methods=["DELETE"],
)
@admin_only
def delete_department_from_course(course_id: str, department_id: str):
    """
    Removes a department from a course.
    """
    course = get_obj(Course, course_id)
    if not course:
        abort(404, description="Course does not exist.")

    department = get_obj(Department, department_id)
    if not department:
        abort(404, description="Department does not exist.")

    course.departments.remove(department)
    db = DatabaseOp()
    db.save(course)

    course_dict = get_course_dict(course)
    return jsonify(course_dict), 200


@app_views.route(
    "/departments/<department_id>/courses/<course_id>",
    strict_slashes=False,
    methods=["DELETE"],
)
@admin_only
def delete_course_from_department(department_id: str, course_id: str):
    """
    Removes a course from a department
    """
    department = get_obj(Department, department_id)
    if not department:
        abort(404, description="Department does not exist.")

    course = get_obj(Course, course_id)
    if not course:
        abort(404, description="Course does not exist.")

    department.courses.remove(course)
    db = DatabaseOp()
    db.save(course)

    course_dict = get_course_dict(course)
    return jsonify(course_dict), 200
