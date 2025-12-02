#!/usr/bin/env python3

"""
Implements routes for CRUD (Create, Read, Update and Delete)
operations on files.
"""


from flask import Flask
from flask.testing import FlaskClient
from typing import Any
import io
import logging
import unittest

from api.v1.app import create_app
from models import storage
from models.course import Course
from models.department import Department
from models.level import Level
from models.user import User
from tests.requests_data import (
    courses_data, levels_data, departments_data
)


logger = logging.getLogger(__name__)


class TestCourseRoute(unittest.TestCase):
    """
    POST - /api/v1/courses/<course_id>/files
    GET - /api/v1/files
    GET - /api/v1/<file_id>
    UPDATE - /api/v1/files/<file_id>
    DELETE - /api/v1/files/<file_id>
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Creates and login an admin user before
        execution of the test methods.
        """
        cls.app: Flask = create_app()
        cls.client: FlaskClient = cls.app.test_client()

        cls.client.post(
            "/api/v1/register",
            json={
                "email": "test@gmail.com",
                "password": "Test1234",
                "is_admin": True
            },
        )
        response = cls.client.post(
            "/api/v1/auth_session/login",
            json={"email": "test@gmail.com", "password": "Test1234"},
        )
        cls.user_id = response.get_json().get("user_id")

        session_cookie = response.headers.get("Set-Cookie")
        if session_cookie:
            cookie_name, session_id = session_cookie.split(
                ";", 1)[0].split("=", 1)
            cls.client.set_cookie(cookie_name, session_id)

    def add_levels(self) -> None:
        """
        Create new levels.
        """
        self.levels = levels_data
        self.level_ids: list[str] = []

        for level in self.levels:
            response = self.client.post("/api/v1/levels", json=level)
            self.level_ids.append(response.get_json().get("id"))

    def add_courses(self) -> None:
        """
        Create new courses.
        """
        self.add_levels()
        self.courses = courses_data
        self.course_ids: list[str] = []

        for index, course in enumerate(self.courses):
            course["level_id"] = self.level_ids[index]
            response = self.client.post(f"/api/v1/courses", json=course)
            self.course_ids.append(response.get_json().get("id"))

    def add_departments(self) -> None:
        """
        Create new departments.
        """
        self.departments = departments_data
        self.dept_ids: list[str] = []

        for dept in self.departments:
            response = self.client.post("/api/v1/departments", json=dept)
            self.dept_ids.append(response.get_json().get("id"))

        for course_id in self.course_ids:
            for dept_id in self.dept_ids:
                self.client.post(
                    f"/api/v1/courses/{course_id}/departments/{dept_id}"
                )

    def delete_levels(self) -> None:
        """
        Delete created levels.
        """
        for level_id in self.level_ids:
            self.client.delete(f"/api/v1/levels/{level_id}")

    def delete_courses(self) -> None:
        """
        Delete created courses.
        """
        for course_id in self.course_ids:
            self.client.delete(f"/api/v1/courses/{course_id}")

    def delete_departments(self) -> None:
        """
        Delete the created departmnets.
        """
        for dept_id in self.dept_ids:
            self.client.delete(f"/api/v1/departments/{dept_id}")

    def setUp(self) -> None:
        """
        Create new files before the execution of each test method.
        """
        self.add_courses()
        self.add_departments()

        self.file_ids: list[str] = []
        self.responses: list[dict[str, Any]] = []

        self.files = [
            (
                io.BytesIO(
                    b"%PDF-1.4\n%Fake PDF content that simulate a real PDF..."
                ),
                "sample1.pdf",
            ),
            (
                io.BytesIO(
                    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR...fake png data..."
                ),
                "sample3.png",
            ),
            (
                io.BytesIO(
                    b"Hello World\nThis is text file content for testing."
                ),
                "sample4.txt",
            ),
            (
                io.BytesIO(
                    b"%PDF-1.4\n%Another fake but bigger PDF content..."
                ),
                "sample5.pdf",
            ),
        ]

        for index, (file_io, filename) in enumerate(self.files):

            data: dict[str, Any] = {
                "file": (file_io, filename),
                "file_type": "lecture material",
                "session": "2024/2025",
                "course_id": self.course_ids[index],
            }

            response = self.client.post(
                f"/api/v1/files",
                data=data,
                content_type="multipart/form-data"
            )
            self.file_ids.append(response.get_json().get("id"))
            self.responses.append(response.get_json())

    def tearDown(self) -> None:
        """
        Deletes created files after each test execution.
        """
        for file_id in self.file_ids:
            self.client.delete(f"/api/v1/files/{file_id}")

        self.delete_courses()
        self.delete_levels()
        self.delete_departments()

        if storage.count(Level):
            raise ValueError("Level deletion was not successful.")
        if storage.count(Course):
            raise ValueError("Course deletion was not successful.")
        if storage.count(Department):
            raise ValueError("Department deletion was not successful.")

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Deletes the admin user after executing the class.
        """
        cls.client.delete(f"/api/v1/users/{cls.user_id}")
        if storage.count(User):
            raise ValueError("Users deletion was not successful")

    def test_add_files(self):
        """
        Test that file metadata is successfully saved
        in the database and the file object uploaded to aws s3 bucket.
        """
        for data in self.responses:
            self.assertIn("id", data)
            self.assertIn("file_name", data)
            self.assertIn("file_type", data)
            self.assertIn("file_ext", data)
            self.assertIn("file_size", data)
            self.assertEqual(data["status"], "pending")
            self.assertIn("course_id", data)
            self.assertIn("user_id", data)
            self.assertNotIn("rejection_reason", data)
            self.assertNotIn("temp_filepath", data)
            self.assertNotIn("permanent_filepath", data)
            self.assertNotIn("admin_id", data)

    def test_get_files_with_pagination(self):
        """
        Verifies all files metadata are returned
        successfully from the database.
        """
        page_size = len(self.files) - 2
        response = self.client.get(
            f"/api/v1/files?page_size={page_size}&page_num=1"
        )

        self.assertEqual(response.status_code, 200)
        self.assertLess(len(response.get_json()), len(self.files))

    def test_get_pending_files(self):
        """
        Verifies that only pending files are returned.
        """
        response = self.client.get("/api/v1/files?search=pending")
        for data in response.get_json():
            self.assertEqual(data.get("status"), "pending")

    def test_get_file(self):
        """
        Test that a presigned url to download or view file
        is returned along with file metadata.
        """
        for file_id in self.file_ids:
            response = self.client.get(f"/api/v1/files/{file_id}")
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertIn("url", data)
            self.assertIn("id", data)
            self.assertIn("file_name", data)
            self.assertIn("file_type", data)
            self.assertIn("file_ext", data)
            self.assertIn("file_size", data)
            self.assertIn("status", data)
            self.assertIn("course_id", data)
            self.assertIn("user_id", data)

    def test_invalid_file_update(self):
        """
        Test that response status code is 400.
        """
        response = self.client.put(
            f"/api/v1/files/{self.file_ids[0]}",
            json={"status": "rejected"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["error"],
            "Rejection reason required for rejected files.",
        )

        response = self.client.put(
            f"/api/v1/files/{self.file_ids[0]}",
            json={"file_type": "past question"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["error"],
            "Past question(s) must have session."
        )

    def test_updated_file(self):
        """
        Test successfule file metadata update.
        """
        response_data = self.responses[0]
        self.assertEqual(response_data["status"], "pending")

        response = self.client.put(
            f"/api/v1/files/{self.file_ids[0]}",
            json={"status": "approved"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json().get("status"),
            "approved"
        )

    def test_delete_rejected_file(self):
        """
        Tests that files with status = 'rejected'
        are deleted from the database
        and s3 bucket.
        """
        response = self.client.put(
            f"/api/v1/files/{self.file_ids[1]}",
            json={
                "status": "rejected",
                "rejection_reason": "Invalid file content."
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.client.get(
                f"/api/v1/files/{self.file_ids[1]}"
            ).status_code, 404
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
