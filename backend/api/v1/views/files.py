#!/usr/bin/env python3

"""
Implements routes for CRUD (Create, Read, Update and Delete)
operations on files.
"""


from dotenv import load_dotenv
from flask import g, abort, jsonify, request
from typing import Any, cast
import logging

from api.v1.views import app_views
from api.v1.auth.authorization import admin_only
from api.v1.utils.utility import get_obj, DatabaseOp
from api.v1.utils.file_utils import FileManager, FileUpload
from models import storage
from models.file import File
from models.notification import Notification
from models.admin import Admin
from models.user import User


logger = logging.getLogger(__name__)
load_dotenv()


def get_file_dict(file: File) -> dict[str, Any]:
    """
    Returns a json serializable dict of the file object.
    """
    if not file:
        return

    file_dict = file.to_dict()

    file_dict["course"] = file.course.course_code
    file_dict["added_by"] = file.added_by.email
    file_dict.pop("temp_filepath", None)
    file_dict.pop("permanent_filepath", None)
    file_dict.pop("__class__", None)

    if file.approved_by:
        file_dict["approved_by"] = file.approved_by.user.email

    return file_dict


def handle_approved_files(file: File, uploader: FileUpload) -> None:
    """
    Move file to permanent S3 bucket if approved.
    """
    new_path: str | None = uploader.upload_file_to_s3_perm(
        file.temp_filepath
    )
    if new_path:
        file.permanent_filepath = new_path
    else:
        file.status = "pending"


def handle_rejected_files(
        file: File, uploader: FileUpload, db: DatabaseOp
) -> None:
    """
    Delete file completely if rejected.
    """
    path: str = file.temp_filepath or file.permanent_filepath
    try:
        uploader.delete_file(path)
        db.delete(file)
        db.commit()
    except Exception:
        return


@app_views.route("/files", strict_slashes=False, methods=["POST"])
def add_file():
    """
    Uploads to temporary s3 bucket waiting for approval of an admin.
    """
    user = cast(User, g.current_user)

    file_upload = FileUpload()
    file_data = file_upload.get_file_and_metadata()

    file_metadata = file_data["file_metadata"]
    file_metadata["user_id"] = user.id

    file = File(**file_metadata)
    db = DatabaseOp()
    db.save(file)

    # upload to s3 bucket
    file_obj = file_data["file_obj"]
    file_upload.upload_file_to_s3_temp(file_obj, file.temp_filepath)

    # notify admins
    db = DatabaseOp()
    notification_data: dict[str, str] = {
        "message": f"new file pending review - {file.file_name}",
        "notification_scope": "admin",
    }
    notification = Notification(**notification_data)
    db.save(notification)

    file_dict: dict[str, str] = get_file_dict(file)
    return jsonify(file_dict), 201


@app_views.route(
        "/files", strict_slashes=False, methods=["GET"]
)
@admin_only
def get_all_files():
    """
    Returns all files in database optionally filtered by:
    - file name
    - file status
    - date created
    - pagination
    """
    page_size = request.args.get("page_size")
    page_num = request.args.get("page_num")
    created_at = request.args.get("date_time")
    file_name = request.args.get("search")
    file_status = request.args.get("file_status")

    if created_at or file_name or file_status:
        files = storage.filter(
            File,
            search_str=file_name,
            file_status=file_status,
            date_str=created_at,
            page_num=page_num,
            page_size=page_size,
        )
    else:
        files = storage.all(
            File,
            page_num=page_num,
            page_size=page_size
        )

    all_files = [get_file_dict(file) for file in files]

    return jsonify(all_files), 200


@app_views.route(
        "/files/<file_id>", strict_slashes=False, methods=["GET"]
)
def get_file(file_id: str):
    """
    Returns file metadata and a presigned url to allow users
    to download or view file.
    """
    file = get_obj(File, file_id)
    if not file:
        abort(404, description="File does not exist.")

    file_upload = FileUpload()
    if file.temp_filepath:
        url = file_upload.get_presigned_url(file.temp_filepath)
    else:
        url = file_upload.get_presigned_url(file.permanent_filepath)

    file_dict = get_file_dict(file)
    file_dict["url"] = url

    return jsonify(file_dict), 200


@app_views.route(
        "/files/<file_id>", strict_slashes=False, methods=["PUT"]
)
@admin_only
def update_file_metadata(file_id: str):
    """
    Updates a file metadata and save in database.
    Moves file to permanent s3 bucket if file status is approved. Or
    Deletes file if file status is rejected.
    """
    admin = cast(Admin, g.current_user.admin)
    uploader = FileUpload()
    db = DatabaseOp()

    file = get_obj(File, file_id)
    if not file:
        abort(400, description="File does not exist")

    file_manager = FileManager()
    metadata = file_manager.validate_update_file_request()
    metadata["admin_id"] = admin.id

    for attr, value in metadata.items():
        setattr(file, attr, value)

    # move to permanent s3 storage
    if file.status == "approved":
        handle_approved_files(file, uploader)
        db.save(file)

    # delete file
    if file.status == "rejected":
        handle_rejected_files(file, uploader, db)

    file_dict: dict[str, str] = get_file_dict(file)
    return jsonify(file_dict), 200


@app_views.route(
        "/files/<file_id>", strict_slashes=False, methods=["DELETE"]
)
@admin_only
def delete_file(file_id: str):
    """
    Delete file from database and aws s3 bucket.
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
