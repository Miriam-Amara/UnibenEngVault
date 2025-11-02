#!/usr/bin/env python3

"""

"""


from flask import request, abort, jsonify
from typing import Any
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils.utility import get_obj, DatabaseOp
from models.course import Course
from models.department import Department
from models.level import Level


logger = logging.getLogger(__name__)


def get_course_departments_dict(course: Course) -> dict[str, list[str]]:
    """
    """
    course_departments = [
        department.dept_code for department in course.departments
    ]
    return {
        "course_code": course.course_code,
        "level": course.level.name,
        "departments": course_departments
    }


def get_department_courses_dict(
        department: Department
    ) -> dict[str, list[str]]:
    """
    """
    dept_courses = [
        course.course_code for course in department.courses
    ]
    return {
        "department_name": department.dept_name,
        "department_code": department.dept_code,
        "department_courses": dept_courses,
    }


def get_department_level_courses_dict(
    department: Department,
    level: Level,
    semester: str | None = None,
) -> list[dict[str, Any]]:
    """
    Return all courses for a given department and level.
    If semester is provided, filter courses by that semester.
    """
    dept_level_courses: list[dict[str, Any]] = []

    for course in department.courses:
        if course.level != level:
            continue

        if semester and course.semester.value != semester:
            continue

        course_dict = course.to_dict()
        course_dict.pop("__class__", None)
        course_dict["course_code"] = course_dict["course_code"].upper()
        course_dict["level"] = course.level.name
        course_dict["files"] = len(course.files)
        course_dict["departments"] = [
            dept.dept_code.upper() for dept in course.departments
        ]

        dept_level_courses.append(course_dict)
    return dept_level_courses


# allow only admins
@app_views.route(
        "/courses/<course_id>/departments/<department_id>",
        methods=["POST"]
    )
@admin_only
def add_course_departments(course_id: str, department_id: str):
    """
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

    course_dict = get_course_departments_dict(course)
    return jsonify(course_dict), 201


# allow only admins
@app_views.route(
        "/departments/<department_id>/courses/<course_id>",
        methods=["POST"]
    )
@admin_only
def add_department_courses(department_id: str, course_id: str):
    """
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

    dept_dict = get_department_courses_dict(department)
    return jsonify(dept_dict), 201


@app_views.route(
        "/courses/<course_id>/departments",
        methods=["GET"]
    )
def get_course_departments(course_id: str):
    """
    """
    course = get_obj(Course, course_id)
    if not course:
        abort(404, description="course does not exist")
    
    course_departments = get_course_departments_dict(course)
    return jsonify(course_departments), 200


@app_views.route(
        "/departments/<department_id>/levels/<level_id>/courses",
        methods=["GET"]
    )
def get_department_level_courses(department_id: str, level_id: str):
    """
    """
    semester = request.args.get("semester")

    if semester and semester.lower().strip() not in ["first", "second"]:
        semester = None
    
    department = get_obj(Department, department_id)
    if not department:
        abort(404, description="Department does not exist.")

    level = get_obj(Level, level_id)
    if not level:
        abort(404, description="Level does not exist.")
    
    department_level_courses = get_department_level_courses_dict(
        department, level, semester=semester
    )

    if not department_level_courses:
        abort(
            404,
            description="No courses found for the department and level"
        )
    return jsonify(department_level_courses), 200


# allow only admins
@app_views.route(
        "/courses/<course_id>/departments/<department_id>",
        methods=["DELETE"]
    )
@admin_only
def delete_course_department(course_id: str, department_id: str):
    """
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
    return jsonify({}), 200


# allow only admins
@app_views.route(
        "/departments/<department_id>/courses/<course_id>",
        methods=["DELETE"]
    )
@admin_only
def delete_department_course(department_id: str, course_id: str):
    """
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
    return jsonify({}), 200
