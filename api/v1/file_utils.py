#!/usr/bin/env python3

"""
"""


from flask import abort, Request
from typing import Any
from uuid import uuid4
from werkzeug.datastructures import FileStorage
import json
import logging
import magic
import os
import re

from models import storage
from models.course import Course
from models.department import Department


logger = logging.getLogger(__name__)


SESSION_PATTERN = r"^\d{4}/\d{4}$"
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 mb
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".pptx", ".png", ".jpg"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
    "application/vnd.openxmlformats-officedocument.presentationml.presentation", # .pptx
    "image/png",
    "image/jpeg"
}

class FileManager:
    """
    """
    def __init__(self, request: Request) -> None:
        self.errors: list[dict[str, Any]] = []
        self.uploaded_files: list[FileStorage] = request.files.getlist("file")


class ValidateRequest(FileManager):
    """
    """
    def metadata_is_json(self, request: Request) -> dict[str, Any]:
        """
        """
        try:
            file_metadata: dict[str, Any] = json.loads(request.form["metadata"])
            logger.debug(f"{file_metadata}")
        except KeyError:
            abort(400, description="Missing key - metadata.")
        except json.JSONDecodeError:
            abort(400, description="Not a valid JSON.")
        return file_metadata
    
    def file_has_filename(self):
        """
        """
        for file_obj in self.uploaded_files:
            if not file_obj.filename:
                abort(400, description="Missing file name")
    
    def file_has_metadata(self, request: Request, file_metadata: dict[str, Any]) -> None:
        """
        """
        if not self.uploaded_files:
            return
        
        logger.debug(f"In ValidateRequest: {self.uploaded_files}")
        logger.debug(f"In ValidateRequest: {file_metadata}")
        valid_files: list[FileStorage] = []
        for file_obj in self.uploaded_files:
            
            file_name = file_obj.filename
            if not file_name:
                return
            if file_name.strip() not in file_metadata:
                self.errors.append({file_name: "Missing metadata"})
                continue
            valid_files.append(file_obj)

        if not valid_files:
            return
        
        self.uploaded_files = valid_files
        logger.debug(f"{self.uploaded_files}")


class ValidateFileMetadata(FileManager):
    """
    """
    def get_metadata(self, file_metadata: dict[str, Any]):
        """
        """
        valid_metadata: dict[str, Any] = {}
        valid_files: list[FileStorage] = []

        for file_obj in self.uploaded_files:

            file_name = file_obj.filename
            if not file_name:
                return

            metadata = file_metadata.get(file_name)
            if not metadata:
                return

            file_type = metadata.get("file_type")
            session = metadata.get("session")
        return file_type, session




class FileUtils:
    """
    """
    def __init__(self, request: Request) -> None:
        self.errors: list[dict[str, Any]] = []
        self.uploaded_files: list[FileStorage] = request.files.getlist("file")

    def read_request(
            self, request: Request
        ) -> dict[str, Any] | None:
        """Reads files and metadata from the request."""
        try:
            # dict: filename -> metadata
            file_metadata: dict[str, Any] = json.loads(request.form["metadata"])
            logger.debug(f"{file_metadata}")
        except KeyError:
            abort(400, description="Missing key - metadata.")
        except json.JSONDecodeError:
            abort(400, description="Not a valid JSON.")

        # Check that each file has metadata
        if not self.uploaded_files:
            return
        
        logger.debug(f"{self.uploaded_files}")
        valid_files: list[FileStorage] = []
        for file_obj in self.uploaded_files:
            filename = file_obj.filename
            if not filename:
                abort(400, description="Missing file name")
            if filename.strip() not in file_metadata:
                self.errors.append({filename: "Missing metadata"})
                continue
            valid_files.append(file_obj)
        if not valid_files:
            return
        
        self.uploaded_files = valid_files
        logger.debug(f"{self.uploaded_files}")
        return file_metadata
    
    def validate_file_metadata(self, file_metadata: dict[str, Any]) -> dict[str, Any] | None:
        """Validates metadata fields for each file."""
        valid_metadata: dict[str, Any] = {}
        valid_files: list[FileStorage] = []

        for file_obj in self.uploaded_files:

            file_name = file_obj.filename
            if not file_name:
                return

            metadata = file_metadata.get(file_name)
            if not metadata:
                return

            file_type = metadata.get("file_type")
            session = metadata.get("session")

            # checks file type (e.g notes, past questions)
            if not file_type:
                self.errors.append({file_name: "metadata missing file_type"})
                continue
            if len(file_type) > 100:
                self.errors.append({file_name: "file_type too long"})
                continue
            
            # checks that past question(s) has session
            metadata["file_type"] = file_type.lower().strip()
            if metadata["file_type"] in ["past question", "past questions"]:
                if not session:
                    self.errors.append({file_name: "past question(s) missing session"})
                    continue
                if not re.match(SESSION_PATTERN, session.strip()):
                    self.errors.append({file_name: "invalid session"})
                    continue

            valid_metadata[file_name] = metadata
            valid_files.append(file_obj)
        
        # keep only valid files
        self.uploaded_files = valid_files
        logger.debug(f"{self.uploaded_files}")
        return valid_metadata
            
    def validate_file(self, file_obj: FileStorage) -> None:
        """Validates individual file properties. Raises exception if invalid."""
        # check file size
        file_obj.seek(0, 2)
        size = file_obj.tell()
        file_obj.seek(0)
        if size > MAX_FILE_SIZE:
            raise ValueError("File too large! Max upload size is 100mb")

        # check file extension
        filename = file_obj.filename
        if not filename:
            raise ValueError("File must have a filename")
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(f"File type {ext} not allowed")

        # 3. Filename sanitation
        if ".." in filename or not re.match(r"^[\w\-. ]+$", filename):
            raise ValueError("Invalid file name")

        # MIME type check
        mime_type = magic.from_buffer(file_obj.read(2048), mime=True)
        file_obj.seek(0)
        if mime_type not in ALLOWED_MIME_TYPES:
            raise ValueError(f"Invalid file format: {mime_type}")

    def process_files(
            self, uploaded_files: list[FileStorage], file_metadata: dict[str, Any]
        ) -> tuple[list[FileStorage], dict[str, Any]]:
        """Validates multiple files and collects errors independently."""
        success_files: list[FileStorage] = []
        failed_files: dict[str, Any] = {}

        for file_obj in uploaded_files:
            filename = file_obj.filename
            if filename not in file_metadata:
                continue

            try:
                self.validate_file(file_obj)
                success_files.append(file_obj)
            except Exception as e:
                failed_files[filename] = str(e)
                self.errors.append({filename: str(e)})

        return success_files, failed_files

    def rename_file(
            self, course: Course, file_obj: FileStorage,
            metadata: dict[str, Any]
        ) -> str | None:
        """
        """
        filename = file_obj.filename
        if not filename:
            return
        
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        file_type = metadata.get("file_type", "unknown").lower().replace(" ", "-")
        session = metadata.get("session", "")
        unique_id = str(uuid4())[:8]
        if session:
            session_safe = session.replace("/", "-")
            new_filename = f"{course.course_code}_{file_type}_{session_safe}_{unique_id}{ext}"
        else:
            new_filename = f"{course.course_code}_{file_type}_{unique_id}{ext}"
        return new_filename

    def generate_s3_filepath(
            self,
            filename: str,
            semester: str,
            course: Course,
            department: Department
        ) -> str | None:
        """
        """
        department_count = storage.count("Department")
        course_count = storage.count_course_departments(course.id)
        
        if not filename or not isinstance(filename, str): # type: ignore
            return
        if not department_count or not isinstance(department_count, int):
            return
        if not course_count:
            return
        
        file_path: str | None = None
        if course_count == department_count:
            file_path = f"temp/{course.level}/{semester}/general/{course.course_code}/{filename}"
        elif course_count > 1 and course_count < department_count:
            file_path = f"temp/{course.level}/{semester}/shared/{course.course_code}/{filename}"
        elif course_count == 1:
            dept_name = department.dept_name.replace(" ", "-")
            file_path = f"temp/{course.level}/{semester}/{dept_name}/{course.course_code}/{filename}"
    
        logger.debug(f"{file_path}")
        return file_path
    
    def get_valid_file(self, request: Request):
        """
        """
        file_metadata = self.read_request(request)
        valid_file_metadata = self.validate_file_metadata(file_metadata)