#!/usr/bin/env python3

"""
"""


from botocore.exceptions import ClientError
from dotenv import load_dotenv
from flask import abort, request
from mypy_boto3_s3 import S3Client
from botocore.config import Config
from mypy_boto3_s3.type_defs import CopySourceTypeDef
from typing import Any, cast
from uuid import uuid4
from werkzeug.datastructures import FileStorage
import boto3
import logging
import magic
import os
import re

from api.v1.utils.data_validations import (
    FileCreate, validate_request_data)
from models import storage
from models.file import File
from models.course import Course
from models.department import Department


logger = logging.getLogger(__name__)
load_dotenv()


MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 mb
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".pptx", ".png", ".jpg", ".txt"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "image/png",
    "image/jpeg",
    "text/plain"
}
FILE_EXTENSION_MAPPING = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "text/plain": ".txt",
}
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
logger.debug(AWS_REGION)
AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')

# if not AWS_ACCESS_KEY_ID:
#     logger.error("No environment variable for aws access key id.")
#     abort(500)
# if not AWS_SECRET_ACCESS_KEY:
#     logger.error("No environment variable for aws secret access key.")
#     abort(500)
# if not AWS_REGION:
#     logger.error("No environment variable for aws region.")
#     abort(500)
# if not AWS_S3_BUCKET:
#     logger.error("No environment variable for aws s3 bucket")
#     abort(500)


def is_valid_file_extension(file_obj: FileStorage) -> str:
    """
    """
    if not isinstance(file_obj, FileStorage): # type: ignore
        abort(
            400,
            description="File must be a valid FileStorage object"
        )
    
    filename = file_obj.filename
    if not filename:
        abort(400, description="File must have a filename")
    
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        abort(400, description=f"File type {ext} not allowed")

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
    """
    if not isinstance(file_obj, FileStorage): # type: ignore
        abort(
            400,
            description="File must be a valid FileStorage object"
        )
    
    size = file_obj.content_length or 0
    if size == 0:
        file_obj.seek(0, 2)
        size = file_obj.tell()
        file_obj.seek(0)

    if size > MAX_FILE_SIZE:
        abort(
            400,
            description=(f"File too large! Max upload size is"
                         f" {MAX_FILE_SIZE/(1024 * 1024)}mb"
                    )
        )
    return size

class FileManager:
    """
    """    
    def validate_file_obj(self) -> dict[str, Any]:
        """
        """
        file_obj = request.files.get("file")

        logger.debug(f"file_obj: {file_obj}")
        if not isinstance(file_obj, FileStorage):
            abort(400, description="Missing or invalid file")

        return {
            "file_size": is_valid_file_size(file_obj),
            "file_ext": is_valid_file_extension(file_obj),
            "file_obj": file_obj
        }
    
    def rename_file(
            self,
            course: Course,
            file_type: str,
            session: str | None,
        ) -> str:
        """
        """
        unique_id = str(uuid4())[:8]
        file_type = file_type.lower().replace(" ", "-")
        file_ext = self.validate_file_obj()["file_ext"]

        if session:
            session_safe = session.replace("/", "-")
            new_filename = (
                f"{course.course_code.upper()}-{file_type}"
                f"-{session_safe}-{unique_id}{file_ext}"
            )
        else:
            new_filename = (
                f"{course.course_code.upper()}-{file_type}-{unique_id}{file_ext}"
            )
        return new_filename

    def generate_temp_s3_filepath(
            self,
            new_filename: str,
            course: Course,
        ) -> str:
        """
        """
        semester = course.semester.value + "-semester"
        department_count = storage.count(Department)
        course_department_count = len(course.departments)
        
        if not department_count:
            department_count = 0

        file_path: str = ""
        if course_department_count == department_count:
            file_path = (
                f"temp/{course.level.name}/{semester}/general/"
                f"{course.course_code.upper()}/{new_filename}"
            )
        elif (
            course_department_count > 1
            and course_department_count < department_count # type: ignore
        ):
            file_path = (
                f"temp/{course.level.name}/{semester}/shared/"
                f"{course.course_code.upper()}/{new_filename}"
            )
        elif course_department_count == 1:
            department: Department = course.departments[0]
            dept_name = department.dept_name.replace(" ", "-")
            file_path = (
                f"temp/{course.level.name}/{semester}/{dept_name}"
                f"/{course.course_code.upper()}/{new_filename}"
            )
    
        return file_path
    
    def generate_permanent_s3_filepath(
            self,
            file_path: str,
        ) -> str:
        """
        """
        parts: list[str] = file_path.split("/")
        parts[0] = ""
        new_file_path = "/".join(parts)

        return new_file_path

    def process_file(
            self, 
            course: Course,
        ) -> dict[str, Any]:
        """
        """
        valid_metadata = validate_request_data(FileCreate)
        if valid_metadata.get("session"):
            session = valid_metadata["session"]
        else:
            session = ""
        
        valid_file = self.validate_file_obj()
        new_filename = self.rename_file(
            course, valid_metadata["file_type"], session
        )
        temp_filepath = self.generate_temp_s3_filepath(new_filename, course)

        file_data: dict[str, Any] = {
            "size": valid_file["file_size"],
            "file_obj": valid_file["file_obj"],
            "file_format": valid_file["file_ext"],
            "session": session,
            "file_type": valid_metadata["file_type"],
            "file_name": new_filename,
            "temp_filepath": temp_filepath,
            "course_id": course.id,
        }
        return file_data
        

class FileUpload:
    """
    """
    s3: S3Client = boto3.client( # type: ignore
        "s3",
        config=Config(signature_version="s3v4"),
        # aws_access_key_id=AWS_ACCESS_KEY_ID,
        # aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        # region_name=AWS_REGION,
    )
    logger.debug(AWS_REGION)
    def get_file_metadata(
            self,
            course: Course,
        ) -> dict[str, Any]:
        """
        """
        file_manager = FileManager()
        file_metadata: dict[str, Any] = file_manager.process_file(course)

        file_obj = file_metadata.pop("file_obj")
        return {
            "file_metadata": file_metadata,
            "file_obj": file_obj
        }
    
    def get_presigned_url(self, s3_key: str):
        """
        Generate a presigned URL for downloading or viewing a file.
        """
        logger.debug(s3_key)
        try:
            presigned_url = self.s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": AWS_S3_BUCKET,
                    "Key": s3_key,
                    "ResponseContentDisposition": f'inline; filename="{s3_key.split("/")[-1]}"'
                },
                ExpiresIn=3600,  # 1 hour
            )
            return presigned_url
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            abort(500)

    def upload_file_to_s3_temp(
            self,
            file_obj: FileStorage,
            course: Course,
            temp_file_path: str
        ) -> None:
        """
        """
        try:
            mime_type = magic.from_buffer(file_obj.read(2048), mime=True)
            file_obj.seek(0)
            self.s3.upload_fileobj(
                file_obj.stream,
                cast(str, AWS_S3_BUCKET),
                temp_file_path,
                ExtraArgs={"ContentType": mime_type}
            )
        except Exception as e:
            logger.error(e)
            abort(500)

    def upload_file_to_s3_perm(self, temp_file_path: str) -> str | None:
        """
        """
        file_manager = FileManager()
        perm_file_path = file_manager.generate_permanent_s3_filepath(
            temp_file_path
        )

        try:
            aws_s3_bucket = cast(str, AWS_S3_BUCKET)
            copy_source: CopySourceTypeDef = {
                "Bucket": aws_s3_bucket,
                "Key": temp_file_path
            }
            self.s3.copy_object(
                Bucket=aws_s3_bucket,
                CopySource=copy_source,
                Key=perm_file_path,
                MetadataDirective='COPY'
            )

            copied_file = self.s3.head_object(
                Bucket=aws_s3_bucket, Key=perm_file_path
            )
            if not copied_file or "ContentLength" not in copied_file:
                raise Exception("Copied file not found or incomplete")
            
            self.s3.delete_object(Bucket=aws_s3_bucket, Key=temp_file_path)
            logger.info(f"Moved file successfully.")

        except ClientError as e:
            logger.error(f"AWS ClientError while moving file: {e}")
            abort(500)
        except Exception as e:
            logger.error(f"Failed to move file: {e}")
            abort(500)

        return perm_file_path

    def delete_file(self, file_path: str):
        """
        """
        aws_s3_bucket = cast(str, AWS_S3_BUCKET)
        try:
            self.s3.delete_object(Bucket=aws_s3_bucket, Key=file_path)
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")


def get_files_by_status(
        status: str, page_size: int, page_num: int
    ) -> list[dict[str, str]]:
    """
    """
    files_list: list[dict[str, str]] = []
    files = storage.all(File, page_size, page_num)

    for file in files:
        if status == "rejected" and file.status.value == "rejected":
            files_list.append(
                {   
                    "id": file.id,
                    "file_name": file.file_name,
                    "status": file.status.value,
                    "rejection_reason": file.rejection_reason
                }
            )
        elif file.status.value == status:
            files_list.append(
                {   
                    "id": file.id,
                    "file_name": file.file_name,
                    "status": file.status.value
                }
            )
    return files_list
