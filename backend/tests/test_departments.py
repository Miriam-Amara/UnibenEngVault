#!/usr/bin/env python3

"""
Implements test cases for department routes.
"""


from flask import Flask
from flask.testing import FlaskClient
from typing import Any
import logging
import unittest

from api.v1.app import create_app
from models import storage
from models.department import Department
from models.user import User
from tests.requests_data import departments_data


logger = logging.getLogger(__name__)


class TestDepartmentRoute(unittest.TestCase):
    """
    POST - /api/v1/departments
    GET - /api/v1/departments
    GET - /api/v1/departments/<dept_id>
    UPDATE - /api/v1/departments/<dept_id>
    DELETE - /api/v1/departments/<dept_id>
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Creates an admin user for the class.
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
            json={
                "email": "test@gmail.com",
                "password": "Test1234"
            },
        )
        cls.user_id = response.get_json().get("user_id")

        session_cookie = response.headers.get("Set-Cookie")
        if session_cookie:
            cookie_name, session_id = session_cookie.split(
                ";", 1)[0].split("=", 1)
            cls.client.set_cookie(cookie_name, session_id)

    def setUp(self) -> None:
        """
        Create departments before each test case execution.
        """
        self.departments = departments_data
        self.dept_ids: list[str] = []
        self.add_dept_responses: list[dict[str, Any]] = []

        for dept in self.departments:
            add_dept_response = self.client.post(
                "/api/v1/departments", json=dept
            )
            self.dept_ids.append(add_dept_response.get_json().get("id"))
            self.add_dept_responses.append(add_dept_response.get_json())

    def tearDown(self) -> None:
        """
        Delete created departments after each test case execution.
        """
        for dept_id in self.dept_ids:
            self.client.delete(f"/api/v1/departments/{dept_id}")
        if storage.count(Department):
            raise ValueError("Departments deletion was not successful.")

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Deletes created admin user after class execution.
        """
        cls.client.delete(f"/api/v1/users/{cls.user_id}")
        if storage.count(User):
            raise ValueError("Users deletion was not successful")

    def test_add_department(self):
        """
        Test that department is created and added
        to the database successfully.
        """
        for department in self.add_dept_responses:
            self.assertIn("dept_name", department)
            self.assertIn("dept_code", department)
            self.assertIn("num_of_courses", department)
            self.assertIn("num_of_users", department)
            self.assertNotIn("__class__", department)

    def test_get_all_departments_with_pagination(self):
        """
        Test the retrieval of departmens by pagination.
        """
        response = self.client.get(
            "/api/v1/departments",
            query_string={"page_size": 5, "page_num": 1}
        )

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.get_json()), 5)

    def test_get_all_departments_without_pagination(self):
        """
        Test the retrieval of all departments without pagination
        i.e page size and page num.
        """
        response = self.client.get("/api/v1/departments")

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(
            len(response.get_json()),
            len(self.departments)
        )

    def test_search_for_departments(self):
        """
        Test the retrieval of all departments
        that matches a search string.
        """
        response = self.client.get(
            "api/v1/departments",
            query_string={"search": "me"}
        )

        self.assertEqual(response.status_code, 200)
        for department in response.get_json():
            self.assertIn("me", department["dept_name"])

    def test_get_department(self):
        """
        Test the retrieval of a given department by its id.
        """
        response = self.client.get(
            f"/api/v1/departments/{self.dept_ids[0]}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("dept_name", response.get_json())
        self.assertIn("dept_code", response.get_json())
        self.assertIn("num_of_users", response.get_json())
        self.assertIn("num_of_courses", response.get_json())

    def test_update_department(self):
        """
        Test that a department is successfully
        updated with new details.
        """
        response = self.client.put(
            f"/api/v1/departments/{self.dept_ids[0]}",
            json={"dept_name": "Medical Engineering"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json().get("dept_name"),
            "medical engineering"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
