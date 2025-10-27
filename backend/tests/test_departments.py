#!/usr/bin/env python3

"""

"""


from flask import Flask
from flask.testing import FlaskClient
import logging
import unittest

from api.v1.app import create_app
from models import storage
from models.department import Department
from models.user import User
from tests.requests_data import department_data


logger = logging.getLogger(__name__)


class TestDepartmentRoute(unittest.TestCase):
    """
    POST - /api/v1/departments
    GET - /api/v1/departments/<int:page_size>/<int:page_num>
    GET - /api/v1/departments/<dept_id>
    UPDATE - /api/v1/departments/<dept_id>
    DELETE - /api/v1/departments/<dept_id>
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
    
    def setUp(self) -> None:
        """
        """
        self.department_data = department_data
        self.dept_ids: list[str] = []

        for data in self.department_data:
            self.response = self.client.post(
                "/api/v1/departments",
                json=data
            )
            self.dept_ids.append(self.response.get_json().get("id"))

    def tearDown(self) -> None:
        """
        """
        for dept_id in self.dept_ids:
            self.client.delete(
                f"/api/v1/departments/{dept_id}"
            )
        if storage.count(Department):
            raise ValueError("Departments deletion was not successful.")
    
    @classmethod
    def tearDownClass(cls) -> None:
        """
        """
        cls.client.delete(
            f"/api/v1/users/{cls.user_id}"
        )
        if storage.count(User):
            raise ValueError("Users deletion was not successful")
        
    def test_add_department(self):
        """
        """
        self.assertEqual(self.response.status_code, 201)
        self.assertIn("dept_code", self.response.get_json())
        self.assertIn("dept_name", self.response.get_json())
        self.assertIn("dept_level_courses_count", self.response.get_json())
        
    def test_get_all_departments_by_pagination(self):
        """
        """
        response = self.client.get("/api/v1/departments/10/1")
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.get_json()), 10)
    
    def test_ge_department(self):
        """
        """
        response = self.client.get(f"/api/v1/departments/{self.dept_ids[0]}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("dept_code", response.get_json())
        self.assertIn("dept_name", response.get_json())
        self.assertIn("dept_level_courses_count", response.get_json())
    
    def test_update_department(self):
        """
        """
        new_data = {"dept_name": "Medical Engineering"}
        response = self.client.put(
            f"/api/v1/departments/{self.dept_ids[0]}",
            json=new_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json().get("dept_name"),
            new_data["dept_name"].lower()
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
