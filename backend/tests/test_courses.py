#!/usr/bin/env python3

"""
Implements unit test cases for courses routes.
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
from tests.requests_data import courses_data, levels_data


logger = logging.getLogger(__name__)


class TestCourseRoute(unittest.TestCase):
    """
    POST - /api/v1/courses
    GET - /api/v1/courses
    GET - /api/v1/courses/<course_id>
    UPDATE - /api/v1/courses/<course_id>
    DELETE - /api/v1/courses/<course_id>
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        Creates and login an admin user before execution of the test methods.
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
        Create new levels.
        """
        self.levels = levels_data
        self.level_ids: list[str] = []

        for level in self.levels:
            response = self.client.post(
                "/api/v1/levels",
                json=level
            )
            self.level_ids.append(response.get_json().get("id"))

    def delete_levels(self) -> None:
        """
        Delete levels created.
        """
        for level_id in self.level_ids:
            self.client.delete(
                f"/api/v1/levels/{level_id}"
            )

    def setUp(self) -> None:
        """
        Create new courses before the execution of each test method.
        """
        self.add_levels()
        self.courses = courses_data
        self.course_ids: list[str] = []
        self.add_course_responses: list[dict[str, Any]] = []

        for index, course in enumerate(self.courses):
            course["level_id"] = self.level_ids[index]
            response = self.client.post(
                f"/api/v1/courses",
                json=course
            )
            self.course_ids.append(response.get_json().get("id"))
            self.add_course_responses.append(response.get_json())

    def tearDown(self) -> None:
        """
        Deletes created courses after each test execution.
        """
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
        Deletes the admin user after executing the class.
        """
        cls.client.delete(
            f"/api/v1/users/{cls.user_id}"
        )
        if storage.count(User):
            raise ValueError("Users deletion was not successful")
    
    def test_add_courses(self):
        """
        Test that a course is successfully created.
        """
        for response_json in self.add_course_responses:
            self.assertIn("course_code", response_json)
    
    def test_get_all_courses(self):
        """
        Test that all courses in the database are returned.
        """
        response = self.client.get("/api/v1/courses")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), len(self.courses))
    
    def test_get_all_courses_with_pagination(self):
        """
        Test that courses retrieval are limited by the page size given.
        """
        response = self.client.get(
            "/api/v1/courses",
            query_string={"page_size": 3, "page_num": 1}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 3)
    
    def test_search_courses_by_course_codes(self):
        """
        Test that only the courses that match the search string are retrieved.
        """
        response = self.client.get(
            "/api/v1/courses",
            query_string={"search_str": "ide"}
        )
        self.assertEqual(response.status_code, 200)

    def test_get_course(self):
        """
        Test that a course is retrieved successfully.
        Verify __class__ is not in the response.
        """
        response = self.client.get(f"/api/v1/courses/{self.course_ids[0]}")

        course_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("course_code", course_data)
        self.assertIn("semester", course_data)
        self.assertIn("credit_load", course_data)
        self.assertIn("title", course_data)
        self.assertIn("outline", course_data)
        self.assertIn("is_active", course_data)
        self.assertIn("level_id", course_data)
        self.assertIn("admin_id", course_data)
        self.assertIn("course_level", course_data)
        self.assertIn("num_of_files_in_course", course_data)
        self.assertIn("course_departments", course_data)
        self.assertIn("added_by", course_data)
        self.assertNotIn("__class__", course_data)

    def test_update_course(self):
        """
        Test that a course is updated successfully.
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
