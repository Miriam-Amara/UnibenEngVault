#!/usr/bin/env python3

"""

"""


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
from tests.requests_data import user_data, department_data, level_data

logger = logging.getLogger(__name__)


class TestUserRoute(unittest.TestCase):
    """
    POST - /api/v1/register
    GET - /api/v1/users/<department_id>/<level_id>/<int:page_size>/<int:page_num>
    GET - /api/v1/users/<user_id>
    UPDATE - /api/v1/users/<user_id>
    DELETE - /api/v1/users/<user_id>
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
    
    def add_departments(self) -> None:
        """
        """
        self.department_data = department_data
        self.dept_ids: list[str] = []

        for data in self.department_data:
            response = self.client.post(
                "/api/v1/departments",
                json=data
            )
            self.dept_ids.append(response.get_json().get("id"))
    
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

    def delete_department(self) -> None:
        """
        """
        for dept_id in self.dept_ids:
            self.client.delete(
                f"/api/v1/departments/{dept_id}"
            )

    def delete_level(self) -> None:
        """
        """
        for level_id in self.level_ids:
            self.client.delete(
                f"/api/v1/levels/{level_id}"
            )

    def setUp(self) -> None:
        """
        """
        self.add_departments()
        self.add_levels()

        self.user_data = user_data
        self.user_ids: list[str] = []
        self.responses: list[dict[str, Any]] = []
        
        for index, user in enumerate(self.user_data):
            user["department_id"] = self.dept_ids[index]
            user["level_id"] = self.level_ids[index]
            response = self.client.post(
                "/api/v1/register", json=user
            )
            self.user_ids.append(response.get_json().get("id"))
            self.responses.append(
                {
                    "status_code": response.status_code,
                     "response_json": response.get_json()
                }
            )

    def tearDown(self) -> None:
        """
        """
        for user_id in self.user_ids:
            self.client.delete(
                f"/api/v1/users/{user_id}"
            )

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
        """
        cls.client.delete(
            f"/api/v1/users/{cls.user_id}"
        )
        if storage.count(User):
            raise ValueError("Users deletion was not successful")
    
    def test_create_user(self):
        """
        """
        for response in self.responses:
            self.assertEqual(response["status_code"], 201)
            self.assertIn("email", response["response_json"])
            self.assertIn("is_admin", response["response_json"])
            self.assertIn("email_verified", response["response_json"])
            self.assertIn("is_active", response["response_json"])
            self.assertIn("warnings_count", response["response_json"])
            self.assertIn("suspensions_count", response["response_json"])
            self.assertIn("department_id", response["response_json"])
            self.assertIn("level_id", response["response_json"])
            self.assertIn("department", response["response_json"])
            self.assertIn("course_files_added", response["response_json"])
            self.assertIn("tutorial_links_added", response["response_json"])
            self.assertIn("feedbacks_added", response["response_json"])
            self.assertIn("helps_added", response["response_json"])
            self.assertIn("reports_added", response["response_json"])
            self.assertNotIn("password", response["response_json"])
    
    def test_get_users_by_department_and_level(self):
        """
        """
        for index, level_id in enumerate(self.level_ids):
            dept_id = self.dept_ids[index]
            response = self.client.get(
                f"/api/v1/users/{dept_id}/{level_id}/5/1"
            )
            self.assertEqual(response.status_code, 200)
            self.assertLessEqual(len(response.get_json()), 5)
    
    def test_get_user(self):
        """
        """
        response = self.client.get(f"/api/v1/users/{self.user_ids[0]}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.get_json())
        self.assertIn("is_admin", response.get_json())
        self.assertIn("email_verified", response.get_json())
        self.assertIn("is_active", response.get_json())
        self.assertIn("warnings_count", response.get_json())
        self.assertIn("suspensions_count", response.get_json())
        self.assertIn("department_id", response.get_json())
        self.assertIn("level_id", response.get_json())
        self.assertIn("department", response.get_json())
        self.assertIn("course_files_added", response.get_json())
        self.assertIn("tutorial_links_added", response.get_json())
        self.assertIn("feedbacks_added", response.get_json())
        self.assertIn("helps_added", response.get_json())
        self.assertIn("reports_added", response.get_json())
        self.assertNotIn("password", response.get_json())
    
    def test_update_user(self):
        """
        """
        user1 = self.client.get(f"/api/v1/users/{self.user_ids[1]}")
        logger.debug(user1.get_json())
        self.assertEqual(user1.get_json().get("is_admin"), False)

        new_data = user1.get_json()
        new_data.update({"is_admin": True})
        logger.debug(new_data)
        response = self.client.put(
            f"/api/v1/users/{self.user_ids[0]}",
            json=new_data
        )
        logger.debug(response.get_json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get("is_admin"), True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
