#!/usr/bin/env python3

"""
Implements file request validations, file uploads,
and file deletions.
"""


from botocore.exceptions import ClientError
from dotenv import load_dotenv
from flask import abort
from mypy_boto3_s3 import S3Client
from botocore.config import Config
from mypy_boto3_s3.type_defs import CopySourceTypeDef
from slugify import slugify
from typing import Any, cast
from werkzeug.datastructures import FileStorage
import boto3
import logging
import magic
import os
import re

from api.v1.utils.data_validations import (
    FileCreate, FileUpdate, validate_form_data
)
from api.v1.utils.utility import get_obj
from models import storage
from models.course import Course
from models.department import Department


logger = logging.getLogger(__name__)
load_dotenv()


MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 mb
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".pptx", ".png", ".jpg", ".txt"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    (
        "application/vnd.openxmlformats-officedocument"
        ".wordprocessingml.document"
    ),
    (
        "application/vnd.openxmlformats-officedocument"
        ".presentationml.presentation"
    ),
    "image/png",
    "image/jpeg",
    "text/plain",
}

pptx = (
    "application/vnd.openxmlformats-officedocument"
    ".presentationml.presentation"
)
docx = (
    "application/vnd.openxmlformats-officedocument"
    ".wordprocessingml.document"
)
FILE_EXTENSION_MAPPING = {
    "application/pdf": ".pdf",
    docx: ".docx",
    pptx: ".pptx",
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "text/plain": ".txt",
}
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")

if not AWS_ACCESS_KEY_ID:
    logger.error("No AWS_ACCESS_KEY_ID environment variable.")
    abort(500)
if not AWS_SECRET_ACCESS_KEY:
    logger.error("No AWS_SECRET_ACCESS_KEY environment variable.")
    abort(500)
if not AWS_REGION:
    logger.error("No AWS_REGION environment variable.")
    abort(500)
if not AWS_S3_BUCKET:
    logger.error("No AWS_S3_BUCKET environment variable.")
    abort(500)


def is_valid_file_extension(file_obj: FileStorage) -> str:
    """
    Checks whether filename is valid and if file extension
    is in allowed file extenstions. Valid file extestions are:
    ".pdf", ".docx", ".pptx", ".png", ".jpg", ".txt"
    """
    if not isinstance(file_obj, FileStorage):  # type: ignore
        abort(400, description="File must be a valid FileStorage object")

    filename = file_obj.filename
    if not filename:
        abort(400, description="File must have a filename")

    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        abort(400, description=f"File extension '{ext}' not allowed")

    if ".." in filename or not re.match(r"^[\w\-. ]+$", filename):
        abort(400, description=f"Invalid file name: {filename}")

    mime_type = magic.from_buffer(file_obj.read(2048), mime=True)
    file_obj.seek(0)
    if mime_type not in ALLOWED_MIME_TYPES:
        abort(400, description=f"Invalid file format: {mime_type}")

    ext = FILE_EXTENSION_MAPPING[mime_type]
    return ext


def is_valid_file_size(file_obj: FileStorage) -> int:
    """
    Verifies that file size does not exceed the max limit.
    """
    if not isinstance(file_obj, FileStorage):  # type: ignore
        abort(400, description="File must be a valid FileStorage object")

    size = file_obj.content_length or 0
    if size == 0:
        file_obj.seek(0, 2)
        size = file_obj.tell()  # in kilobyte
        file_obj.seek(0)

    if size > MAX_FILE_SIZE:
        abort(
            400,
            description=(
                f"File too large! Max upload size is"
                f" {MAX_FILE_SIZE/(1024 * 1024)}mb"
            ),
        )
    return size


class FileManager:
    """
    Implements methods for validating files,
    renaming and generating file paths.
    """

    def validate_file_obj_and_metadata(self) -> dict[str, Any]:
        """
        Checks whether file data and object is valid. Validates:
        - file metadata
        - file is an instance of FileStorage class
        - file size
        - file extension

        Returns:
        - file size
        - file extension
        - file object
        - file metadata
        """
        valid_metadata, file_obj = validate_form_data(FileCreate)

        if not isinstance(file_obj, FileStorage):
            abort(400, description="File missing.")

        if valid_metadata.get("session"):
            session = valid_metadata["session"]
        else:
            session = ""

        if (
            valid_metadata["file_type"] in ["past_question", "past_questions"]
            and not session
        ):
            abort(400, "Past question(s) must have session.")

        course: Course | None = get_obj(Course, valid_metadata["course_id"])
        if not course:
            abort(404, description="Course not found.")

        valid_metadata["course"] = course

        return {
            "file_size": is_valid_file_size(file_obj),
            "file_ext": is_valid_file_extension(file_obj),
            "file_obj": file_obj,
            "file_metadata": valid_metadata,
        }

    def validate_update_file_request(self) -> dict[str, Any]:
        """
        Validates file metadata from update file requests.
        """
        valid_metadata = validate_form_data(FileUpdate)[0]

        file_type = valid_metadata.get("file_type")
        session = valid_metadata.get("session")
        course_id = valid_metadata.get("course")
        status = valid_metadata.get("status")
        rejection_reason = valid_metadata.get("rejection_reason")

        if file_type in ["past question", "past questions"] and not session:
            abort(400, description="Past question(s) must have session.")

        if status == "rejected" and not rejection_reason:
            abort(
                400,
                description="Rejection reason required for rejected files."
            )

        if course_id:
            course = get_obj(Course, course_id)
            if not course:
                abort(400, description="Course does not exist.")

        return valid_metadata

    def rename_file(self, original_filename: str, ext: str) -> str:
        """
        Renames a clean, safe and properly formatted filename.
        """
        name = os.path.splitext(original_filename)[0]
        new_filename = slugify(name, separator="-") + ext

        return new_filename

    def generate_temp_s3_filepath(
        self,
        new_filename: str,
        course: Course,
    ) -> str:
        """
        Returns a temporary file path that will be added to
        temporary s3 bucket awaiting approval of an admin.
        """
        semester = course.semester.value + "-semester"
        department_count = storage.count(Department)
        course_departments_count = len(course.departments)

        if not department_count:
            department_count = 0

        if not course_departments_count:
            abort(
                400,
                description=(
                    "Please add courses to departments"
                    " before uploading file."
                ),
            )

        file_path: str = ""

        # course offered by all departments.
        if course_departments_count == department_count:
            file_path = (
                f"temp/{course.level.level_name}/{semester}/general/"
                f"{course.course_code.upper()}/{new_filename}"
            )
        # course shared by some departments.
        elif (
            course_departments_count > 1
            and course_departments_count < department_count  # type: ignore
        ):
            file_path = (
                f"temp/{course.level.level_name}/{semester}/shared/"
                f"{course.course_code.upper()}/{new_filename}"
            )
        # course offered by exactly one department.
        elif course_departments_count == 1:
            department: Department = course.departments[0]
            dept_name = department.dept_name.replace(" ", "-")
            file_path = (
                f"temp/{course.level.level_name}/{semester}/{dept_name}"
                f"/{course.course_code.upper()}/{new_filename}"
            )

        return file_path

    def generate_permanent_s3_filepath(
        self,
        file_path: str,
    ) -> str:
        """
        Returns permanent file path to be added to permanent s3 bucket
        after an admin's approval.
        """
        parts: list[str] = file_path.split("/")
        parts[0] = ""
        new_file_path = "/".join(parts)

        return new_file_path

    def process_file(
        self,
    ) -> dict[str, Any]:
        """
        Processes file validation and returns file object and metadata.
        """
        valid_data = self.validate_file_obj_and_metadata()
        file_extension: str = valid_data["file_ext"]
        file_obj: FileStorage = valid_data["file_obj"]
        file_size: int = valid_data["file_size"]
        file_metadata = valid_data["file_metadata"]

        original_filename = file_obj.filename
        course: Course = file_metadata.get("course")
        file_type = file_metadata.get("file_type")
        session = file_metadata.get("session")

        if not original_filename:
            abort(400, description="File missing filename")

        new_filename = self.rename_file(original_filename, file_extension)
        temp_filepath = self.generate_temp_s3_filepath(new_filename, course)

        file_data: dict[str, Any] = {
            "file_obj": file_obj,
            "file_name": new_filename,
            "file_type": file_type,
            "file_ext": file_extension,
            "file_size": file_size,
            "session": session,
            "temp_filepath": temp_filepath,
            "course": course,
            "course_id": course.id,
        }
        return file_data


class FileUpload:
    """ """

    s3: S3Client = boto3.client(  # type: ignore
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
        config=Config(signature_version="s3v4"),
    )

    def get_file_and_metadata(self) -> dict[str, Any]:
        """
        Returns file metadata and file object.
        """
        file_manager = FileManager()
        file_metadata: dict[str, Any] = file_manager.process_file()

        file_obj = file_metadata.pop("file_obj")
        return {"file_metadata": file_metadata, "file_obj": file_obj}

    def get_presigned_url(self, s3_key: str):
        """
        Generate a presigned URL for downloading or viewing a file.
        """
        try:
            filename = f'inline; filename="{s3_key.split("/")[-1]}"'
            presigned_url = self.s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": AWS_S3_BUCKET,
                    "Key": s3_key,
                    "ResponseContentDisposition": filename,
                },
                ExpiresIn=3600,  # 1 hour
            )
            return presigned_url
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            abort(500)

    def upload_file_to_s3_temp(
        self, file_obj: FileStorage, temp_file_path: str
    ) -> None:
        """
        Uploads file to temporary s3 bucket.
        """
        try:
            head_bytes = file_obj.stream.read(2048)
            mime_type = magic.from_buffer(head_bytes, mime=True)
            file_obj.stream.seek(0)

            self.s3.upload_fileobj(
                file_obj.stream,
                cast(str, AWS_S3_BUCKET),
                temp_file_path,
                ExtraArgs={"ContentType": mime_type},
            )

        except Exception as e:
            logger.error(e)
            raise
            # abort(500)

    def upload_file_to_s3_perm(self, temp_file_path: str) -> str | None:
        """
        Uploads file to permanent s3 bucket.
        """
        file_manager = FileManager()
        perm_file_path = file_manager.generate_permanent_s3_filepath(
            temp_file_path
        )

        try:
            aws_s3_bucket = cast(str, AWS_S3_BUCKET)
            copy_source: CopySourceTypeDef = {
                "Bucket": aws_s3_bucket,
                "Key": temp_file_path,
            }
            self.s3.copy_object(
                Bucket=aws_s3_bucket,
                CopySource=copy_source,
                Key=perm_file_path,
                MetadataDirective="COPY",
            )

            copied_file = self.s3.head_object(
                Bucket=aws_s3_bucket,
                Key=perm_file_path
            )
            if not copied_file or "ContentLength" not in copied_file:
                raise Exception("Copied file not found or incomplete")

            self.s3.delete_object(Bucket=aws_s3_bucket, Key=temp_file_path)
            logger.info(f"Moved file successfully.")
            return perm_file_path
        except ClientError as e:
            logger.error(f"AWS ClientError while moving file: {e}")
            return
        except Exception as e:
            logger.error(f"Failed to move file: {e}")
            return

    def delete_file(self, file_path: str):
        """
        Deletes file from s3 bucket.
        """
        aws_s3_bucket = cast(str, AWS_S3_BUCKET)
        try:
            self.s3.delete_object(Bucket=aws_s3_bucket, Key=file_path)
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            raise
