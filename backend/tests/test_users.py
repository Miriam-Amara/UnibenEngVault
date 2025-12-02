#!/usr/bin/env python3

"""
Implements test cases for users routes.
"""

from datetime import datetime
from flask import Flask
from flask.testing import FlaskClient
from typing import Any, cast
import logging
import unittest

from api.v1.app import create_app
from models import storage
from models.user import User
from models.department import Department
from models.level import Level
from tests.requests_data import (
    users_data, departments_data, levels_data
)

logger = logging.getLogger(__name__)


class TestUserRoute(unittest.TestCase):
    """
    POST - /api/v1/register
    GET - /api/v1/users/<department_id>/<level_id>
    GET - /api/v1/users/<user_id>
    UPDATE - /api/v1/users/<user_id>
    DELETE - /api/v1/users/<user_id>
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

        cls.login_response = cls.client.post(
            "/api/v1/auth_session/login",
            json={
                "email": "test@gmail.com",
                "password": "Test1234"
            },
        )
        cls.user_id = cls.login_response.get_json().get("user_id")

        session_cookie = cls.login_response.headers.get("Set-Cookie")
        if session_cookie:
            cookie_name, session_id = session_cookie.split(
                ";", 1)[0].split("=", 1)
            cls.client.set_cookie(cookie_name, session_id)

    def add_departments(self) -> None:
        """
        Create new departments.
        """
        self.departments = departments_data
        self.dept_ids: list[str] = []

        for department in self.departments:
            dept_response = self.client.post(
                "/api/v1/departments",
                json=department
            )
            self.dept_ids.append(dept_response.get_json().get("id"))

    def add_levels(self) -> None:
        """
        Create new levels.
        """
        self.levels = levels_data
        self.level_ids: list[str] = []

        for level in self.levels:
            level_response = self.client.post(
                "/api/v1/levels", json=level
            )
            self.level_ids.append(level_response.get_json().get("id"))

    def delete_department(self) -> None:
        """
        Delete the created departments.
        """
        for dept_id in self.dept_ids:
            self.client.delete(f"/api/v1/departments/{dept_id}")

    def delete_level(self) -> None:
        """
        Delete the created levels.
        """
        for level_id in self.level_ids:
            self.client.delete(f"/api/v1/levels/{level_id}")

    def setUp(self) -> None:
        """
        Create users before the execution of each test methods.
        """
        self.add_departments()
        self.add_levels()

        self.users = users_data
        self.user_ids: list[str] = []
        self.register_responses: list[dict[str, Any]] = []

        for index, user in enumerate(self.users):
            user["department_id"] = self.dept_ids[index]
            user["level_id"] = self.level_ids[index]
            response = self.client.post("/api/v1/register", json=user)
            self.user_ids.append(response.get_json().get("id"))
            self.register_responses.append(
                {
                    "status_code": response.status_code,
                    "response_json": response.get_json(),
                }
            )

    def tearDown(self) -> None:
        """
        Delete users after the execution of each test methods.
        """
        for user_id in self.user_ids:
            self.client.delete(f"/api/v1/users/{user_id}")

        self.delete_department()
        self.delete_level()

        if cast(int, storage.count(User)) > 1:
            raise ValueError("Users deletion was not successful.")
        if storage.count(Department):
            raise ValueError("Departments deletion was not successful.")
        if storage.count(Level):
            raise ValueError("Levels deletion was not successful.")

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Deletes the admin user after executing the class.
        """
        cls.client.delete(f"/api/v1/users/{cls.user_id}")
        if storage.count(User):
            raise ValueError("Users deletion was not successful")

    def test_create_user(self):
        """
        Test that users are created successfully.
        """
        for response in self.register_responses:
            user_data = response["response_json"]
            self.assertEqual(response["status_code"], 201)
            self.assertIn("email", user_data)
            self.assertIn("is_admin", user_data)
            self.assertIn("email_verified", user_data)
            self.assertIn("is_active", user_data)
            self.assertIn("warnings_count", user_data)
            self.assertIn("suspensions_count", user_data)
            self.assertIn("department_id", user_data)
            self.assertIn("level_id", user_data)
            self.assertIn("department", user_data)
            self.assertIn("course_files_added", user_data)
            self.assertIn("tutorial_links_added", user_data)
            self.assertIn("feedbacks_added", user_data)
            self.assertIn("helps_added", user_data)
            self.assertIn("reports_added", user_data)
            self.assertNotIn("password", user_data)

    def test_get_user_by_id(self):
        """
        Test get a user by user id.
        Verify password is not in the returned json.
        """
        response = self.client.get(f"/api/v1/users/{self.user_ids[0]}")
        user_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("email", user_data)
        self.assertIn("is_admin", user_data)
        self.assertIn("email_verified", user_data)
        self.assertIn("is_active", user_data)
        self.assertIn("warnings_count", user_data)
        self.assertIn("suspensions_count", user_data)
        self.assertIn("department_id", user_data)
        self.assertIn("level_id", user_data)
        self.assertIn("department", user_data)
        self.assertIn("course_files_added", user_data)
        self.assertIn("tutorial_links_added", user_data)
        self.assertIn("feedbacks_added", user_data)
        self.assertIn("helps_added", user_data)
        self.assertIn("reports_added", user_data)
        self.assertNotIn("password", user_data)

    def test_get_user_by_me(self):
        """
        Test that the get me route returns the current user.
        """
        response = self.client.get(f"/api/v1/users/me")
        current_user = response.get_json().get("id")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            current_user,
            self.login_response.get_json().get("user_id")
        )

    def test_get_users_filtered_by_department_and_level(self):
        """
        Test the retrieval of users in a specific department and level.
        """
        for index, level_id in enumerate(self.level_ids):
            dept_id = self.dept_ids[index]
            response = self.client.get(
                f"/api/v1/users/{dept_id}/{level_id}?page_size=5&page_num=1"
            )
            self.assertEqual(response.status_code, 200)
            self.assertLessEqual(len(response.get_json()), 5)

    def test_get_users_filtered_by_date(self):
        """
        Test the retrieval of users created on a specific date.
        """
        created_at = (
            self.client.get(f"/api/v1/users/{self.user_ids[0]}")
            .get_json()
            .get("created_at")
        )
        date_only = datetime.fromisoformat(created_at).date()

        filtered_responses = self.client.get(
            "/api/v1/users", query_string=created_at
        )
        self.assertEqual(filtered_responses.status_code, 200)

        for response_data in filtered_responses.get_json():
            date_part = datetime.fromisoformat(
                response_data.get("created_at")
            ).date()
            self.assertEqual(date_part, date_only)

    def test_update_user(self):
        """
        Test that a user's details is updated successfully.
        """
        get_user_response = self.client.get(
            f"/api/v1/users/{self.user_ids[1]}"
        )

        user_data = get_user_response.get_json()
        self.assertFalse(user_data.get("is_admin"))

        user_data.update({"is_admin": True})
        update_user_response = self.client.put(
            f"/api/v1/users/{self.user_ids[1]}", json=user_data
        )
        self.assertEqual(update_user_response.status_code, 200)
        self.assertTrue(
            update_user_response.get_json().get("is_admin")
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
