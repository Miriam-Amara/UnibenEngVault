#!/usr/bin/env python3

"""

"""


from flask import Flask
from flask.testing import FlaskClient
from typing import Any
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
    POST - /api/v1/courses
    GET - /api/v1/courses/<int:page_size>/<int:page_num>
    GET - /api/v1/courses/<course_id>
    UPDATE - /api/v1/courses/<course_id>
    DELETE - /api/v1/courses/<course_id>
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
        self.add_levels()
        self.course_data = course_data
        self.course_ids: list[str] = []
        self.responses: list[dict[str, Any]] = []

        for index, data in enumerate(self.course_data):
            data["level_id"] = self.level_ids[index]
            self.response = self.client.post(
                f"/api/v1/courses",
                json=data
            )
            self.course_ids.append(self.response.get_json().get("id"))
            self.responses.append(
                {
                    "status_code": self.response.status_code,
                    "response_json": self.response.get_json()
                }
            )

    def tearDown(self) -> None:
        """
        """
        logger.debug(self.course_ids)
        for course_id in self.course_ids:
            self.client.delete(
                f"/api/v1/courses/{course_id}"
            )

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
    
    def test_add_courses(self):
        """
        """
        for response in self.responses:
            self.assertEqual(response["status_code"], 201)

    def test_get_courses(self):
        """
        """
        response = self.client.get(f"/api/v1/courses/{self.course_ids[0]}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("course_code", response.get_json())
        self.assertIn("semester", response.get_json())
        self.assertIn("credit_load", response.get_json())
        self.assertIn("title", response.get_json())
        self.assertIn("outline", response.get_json())
        self.assertIn("is_active", response.get_json())
        self.assertIn("level_id", response.get_json())
        self.assertIn("admin_id", response.get_json())
        self.assertIn("files", response.get_json())
        self.assertIn("departments", response.get_json())

    def test_update_course(self):
        """
        """
        course = self.client.get(f"/api/v1/courses/{self.course_ids[0]}")
        self.assertEqual(course.get_json().get("semester"), "first")

        new_data = {"semester": "second"}
        response = self.client.put(
            f"/api/v1/courses/{self.course_ids[0]}",
            json=new_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get("semester"), new_data["semester"])



if __name__ == "__main__":
    unittest.main(verbosity=2)
