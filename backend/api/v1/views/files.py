#!/usr/bin/env python3

"""

"""


from copy import deepcopy
from dotenv import load_dotenv
from flask import g, abort, jsonify
from typing import Any, cast
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils.utility import get_obj, DatabaseOp
from api.v1.utils.data_validations import validate_request_data, FileUpdate
from api.v1.utils.file_utils import FileUpload, get_files_by_status
from models.course import Course
from models.file import File
from models.notification import Notification
from models.user import User


logger = logging.getLogger(__name__)
load_dotenv()


def get_file_dict(file: File) -> dict[str, Any]:
    """
    """
    file_dict = deepcopy(file.to_dict())
    new_file_dict: dict[str, Any] = {}
    new_file_dict["id"] = file_dict.pop("id", None)
    new_file_dict["file_name"] = file_dict.pop("file_name", None)
    new_file_dict["status"] = file_dict.pop("status", None)
    return new_file_dict


@app_views.route(
        "/courses/<course_id>/files",
        strict_slashes=False,
        methods=["POST"]
    )
def upload_file(course_id: str):
    """
    """
    user = cast(User, g.current_user)

    course = get_obj(Course, course_id)
    if not course:
        abort(404, description="Course does not exist.")
    
    file_upload = FileUpload()
    file_info = file_upload.get_file_metadata(course)
    file_metadata = file_info["file_metadata"]
    file_metadata["added_by"] = user

    file_record = File(**file_metadata)
    db = DatabaseOp()
    db.save(file_record)    
    
    # upload to s3 bucket
    file_obj = file_info["file_obj"]
    file_upload.upload_file_to_s3_temp(file_obj, course, file_record.temp_filepath)

    # notify admins
    db = DatabaseOp()
    notification_data: dict[str, str] = {
        "message": f"new file pending review - {file_record.file_name}",
        "notification_scope": "admin",
    }
    notification = Notification(**notification_data)
    db.save(notification)

    file_dict: dict[str, str] = get_file_dict(file_record)
    return jsonify(file_dict), 201


# allow only admins
@app_views.route(
        "/files/<status>/<int:page_size>/<int:page_num>",
        strict_slashes=False,
        methods=["GET"]
)
@admin_only
def get_all_files_by_status(status: str, page_size: int, page_num: int):
    """
    """

    files = get_files_by_status(
        status, page_size, page_num
    )
    return jsonify(files), 200


@app_views.route(
        "/courses/<course_id>/files/approved",
        strict_slashes=False,
        methods=["GET"]
)
def get_approved_course_files(course_id: str):
    """
    """
    course = get_obj(Course, course_id)
    if not course:
        abort(404, description="Course does not exist.")

    course_files: list[dict[str, str]] = [
        get_file_dict(file) 
        for file in course.files if file.status.value == "approved"
    ]
    return jsonify(course_files), 200


@app_views.route("/<file_id>", strict_slashes=False, methods=["GET"])
def serve_file(file_id: str):
    """
    """
    file = get_obj(File, file_id)
    if not file:
        abort(404, description="File does not exist.")

    file_upload = FileUpload()
    url = file_upload.get_presigned_url(file.file_name)
    return jsonify({"url": url}), 200


# allow only admins
@app_views.route(
        "/files/<file_id>",
        strict_slashes=False,
        methods=["PUT"]
    )
@admin_only
def update_file_metadata(file_id: str):
    """
    """
    file = get_obj(File, file_id)
    if not file:
        abort(400, description="File does not exist")
    
    logger.debug(f"In update route")
    valid_metadata= validate_request_data(FileUpdate)
    logger.debug(f"valid metadata: {valid_metadata}")
    for attr, value in valid_metadata.items():
        setattr(file, attr, value)
    
    # move to permanent s3 storage
    file_upload = FileUpload()
    if file.status.value == "approved":
        perm_filepath: str | None = file_upload.upload_file_to_s3_perm(
            file.temp_filepath
        )
        if perm_filepath:
            file.permanent_filepath = perm_filepath
        else:
            file.status = "pending"

    db = DatabaseOp()
    db.save(file)

    file_dict: dict[str, str] = get_file_dict(file)
    return jsonify(file_dict), 200


# allow only admins
@app_views.route(
        "/files/<file_id>",
        strict_slashes=False,
        methods=["DELETE"]
    )
@admin_only
def delete_file(file_id: str):
    """
    """
    file = get_obj(File, file_id)
    if not file:
        abort(404, description="File does not exist")

    file_upload = FileUpload()

    if file.status.value == "approved":
        file_upload.delete_file(file.permanent_filepath)
    else:
        file_upload.delete_file(file.temp_filepath)
    
    db = DatabaseOp()
    db.delete(file)
    db.commit()
    return jsonify({}), 200
