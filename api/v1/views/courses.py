#!/usr/bin/env python3

"""

"""


from flask import g, abort, jsonify
from typing import cast
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils import get_obj
from api.v1.data_validations import ValidateData, DatabaseOp
from models import storage
from models.course import Course
from models.admin import Admin


logger = logging.getLogger(__name__)


# allow only admins
@app_views.route("/admins/levels/<level_id>/courses", strict_slashes=False, methods=["POST"])
@admin_only
def create_course(level_id: str):
    """
    """
    admin = cast(Admin, g.current_user.admin)
    logger.debug(f"Admin: {admin.to_dict()}")
    data_validator = ValidateData()
    validated_data = data_validator.validate_request_data("CourseCreate")
    if not validated_data:
        logger.error("Invalid validation class name.")
        abort(500)
    
    level = get_obj("Level", level_id)
    if not level:
        abort(404, description="Level does not exist.")
    
    validated_data["admin_id"] = admin.id
    validated_data["level_id"] = level.id
    db = DatabaseOp()
    course = Course(**validated_data)
    db.save(course)

    course_dict = course.to_dict()

    logger.debug(f"{course_dict}")
    return jsonify(course_dict), 201

# allow only admins
@app_views.route("/admins/levels/<level_id>/courses/<int:page_size>/<int:page_num>", methods=["GET"])
@admin_only
def get_courses(level_id: str, page_size: int, page_num: int):
    """
    """
    level = get_obj("Level", level_id)
    if not level:
        abort(404, description="Level does not exist.")

    course_objects = storage.all(page_size, page_num, "Course")
    if not course_objects:
        abort(404, description="No courses found for the level.")
    
    all_courses = [course.to_dict() for course in course_objects]
    logger.debug(f"{all_courses}")
    return jsonify(all_courses), 200

# allow only admins
@app_views.route("admins/levels/<level_id>/courses/<course_id>", methods=["GET"])
@admin_only
def get_course(level_id: str, course_id: str):
    """
    """
    level = get_obj("Level", level_id)
    if not level:
        abort(404, description="Level does not exist.")

    course = get_obj("Course", course_id)
    if not course:
        abort(404, description="Course does not exist for the level.")

    logger.debug(f"{course.to_dict()}")
    return jsonify(course.to_dict()), 200

# allow only admins
@app_views.route("admins/levels/<level_id>/courses/<course_id>", methods=["PUT"])
@admin_only
def update_course(level_id: str, course_id: str):
    """
    """
    data_validator = ValidateData()
    validated_data = data_validator.validate_request_data("CourseUpdate")
    if not validated_data:
        logger.error("Invalid validation class name.")
        abort(500)
    
    level = get_obj("Level", level_id)
    course = get_obj("Course", course_id)
    if not level:
        abort(404, description="Level does not exist.")
    if not course:
        abort(404, description="Course does not exist for the level.")
    

    for attr, value in validated_data.items():
        setattr(course, attr, value)
    
    db = DatabaseOp()
    db.save(course)
    
    logger.debug(f"{course.to_dict()}")
    return jsonify(course.to_dict()), 200

# allow only admins
@app_views.route("admins/levels/<level_id>/courses/<course_id>", methods=["DELETE"])
@admin_only
def delete_course(level_id: str, course_id: str):
    """
    """
    level = get_obj("Level", level_id)
    course = get_obj("Course", course_id)
    if not level:
        abort(404, description="Level does not exist.")
    if not course:
        abort(404, description="Course does not exist for the level.")

    db = DatabaseOp()
    db.delete(course)
    db.commit()
    return jsonify({}), 200
