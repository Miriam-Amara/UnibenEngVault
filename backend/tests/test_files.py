#!/usr/bin/env python3

"""

"""


from flask import Flask
from flask.testing import FlaskClient
from typing import Any
import io
import json
import logging
import unittest

from api.v1.app import create_app
from models import storage
from models.course import Course
from models.level import Level
from models.user import User
from tests.requests_data import course_data, level_data


logger = logging.getLogger(__name__)


class TestCourseRoute(unittest.TestCase):
    """
    POST - /api/v1/courses/<course_id>/files
    GET - /api/v1/files/<status>/<int:page_size>/<int:page_num>
    GET - /api/v1/courses/<course_id>/files/approved
    GET - /api/v1/<file_id>
    UPDATE - /api/v1/files/<file_id>
    DELETE - /api/v1/files/<file_id>
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        """
        cls.app: Flask = create_app()
        cls.client: FlaskClient = cls.app.test_client()

        cls.client.post(
            "/api/v1/register",
            json={
                "email": "test@gmail.com",
                "password": "Test1234",
                "is_admin": True
            }
        )
        response = cls.client.post(
            "/api/v1/auth_session/login",
            json={"email": "test@gmail.com", "password": "Test1234"}
        )
        cls.user_id = response.get_json().get("user_id")

        session_cookie = response.headers.get("Set-Cookie")
        if session_cookie:
            cookie_name, session_id = (
                session_cookie.split(";", 1)[0].split("=", 1)
            )
            cls.client.set_cookie(cookie_name, session_id)
    
    def add_courses(self) -> None:
        """
        """
        self.add_levels()
        self.course_data = course_data
        self.course_ids: list[str] = []

        for index, data in enumerate(self.course_data):
            data["level_id"] = self.level_ids[index]
            self.response = self.client.post(
                f"/api/v1/courses",
                json=data
            )
            self.course_ids.append(self.response.get_json().get("id"))

    def add_levels(self) -> None:
        """
        """
        self.level_data = level_data
        self.level_ids: list[str] = []

        for data in self.level_data:
            response = self.client.post(
                "/api/v1/levels",
                json=data
            )
            self.level_ids.append(response.get_json().get("id"))
    
    def delete_courses(self) -> None:
        """
        """
        for course_id in self.course_ids:
            self.client.delete(
                f"/api/v1/courses/{course_id}"
            )

    def delete_levels(self) -> None:
        """
        """
        for level_id in self.level_ids:
            self.client.delete(
                f"/api/v1/levels/{level_id}"
            )

    def setUp(self) -> None:
        """
        """
        self.add_courses()
        self.file_ids: list[str] = []
        self.responses: list[dict[str, Any]] = []
        files = [
            "sample1.pdf", "sample2.pdf", "sample3.pdf",
            "sample4.pdf", "sample5.pdf"
        ]

        data: dict[str, Any] = {
            "file": (io.BytesIO(b"%PDF-1.4\n%Fake PDF content"), "sample.pdf"),
            "metadata": json.dumps({
                "file_type": "lecture material",
                "session": "2024/2025"
            })
        }
    
        for index, course_id in enumerate(self.course_ids):
            data["file"] = (io.BytesIO(b"test content"), f"{files[index]}")
            response = self.client.post(
                f"/api/v1/courses/{course_id}/files",
                data=data,
                content_type="multipart/form-data"
            )
            self.file_ids.append(response.get_json().get("id"))
            self.responses.append(
                {
                    "status_code": response.status_code,
                    "response_json": response.get_json()
                }
            )
        
    def tearDown(self) -> None:
        """
        """
        for file_id in self.file_ids:
            self.client.delete(
                f"/api/v1/files/{file_id}"
            )

        self.delete_courses()
        self.delete_levels()
        if storage.count(Level):
            raise ValueError("Level deletion was not successful.")
        if storage.count(Course):
            raise ValueError("Course deletion was not successful.")
    
    @classmethod
    def tearDownClass(cls) -> None:
        """
        """
        cls.client.delete(
            f"/api/v1/users/{cls.user_id}"
        )
        if storage.count(User):
            raise ValueError("Users deletion was not successful")
    
    def test_add_files(self):
        """
        """
        for response in self.responses:
            self.assertEqual(response["status_code"], 201)
            self.assertIn("id", response["response_json"])
            self.assertIn("file_name", response["response_json"])
            self.assertIn("status", response["response_json"])

    def test_get_files_by_status(self):
        """
        """
        statuses = ["pending", "rejected", "approved"]

        for status in statuses:
            response = self.client.get(
                f"/api/v1/files/{status}/10/1"
            )
            self.assertEqual(response.status_code, 200)
            self.assertLessEqual(len(response.get_json()), 10)
            
    def test_get_approved_course_files(self):
        """
        """
        for course_id in self.course_ids:
            response = self.client.get(
                f"/api/v1/courses/{course_id}/files/approved"
            )
            self.assertEqual(response.status_code, 200)
    
    def test_get_file_presigned_url(self):
        """
        """
        for file_id in self.file_ids:
            response = self.client.get(f"/api/v1/{file_id}")
            self.assertEqual(response.status_code, 200)

    def test_updated_file(self):
        """
        """
        for response in self.responses:
            self.assertEqual(response["response_json"]["status"], "pending")

        new_data = {"status": "approved"}
        for file_id in self.file_ids:
            response = self.client.put(
                f"/api/v1/files/{file_id}",
                json=new_data
            )
            import json
            logger.debug(json.dumps(response.get_json(), indent=4))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json().get("status"), "approved")
