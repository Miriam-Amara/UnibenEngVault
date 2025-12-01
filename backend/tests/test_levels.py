#!/usr/bin/env python3

"""
Implements test cases for level routes.
"""


from flask import Flask
from flask.testing import FlaskClient
import logging
import unittest

from api.v1.app import create_app
from models import storage
from models.user import User
from models.level import Level
from tests.requests_data import levels_data

logger = logging.getLogger(__name__)


class TestLevelRoute(unittest.TestCase):
    """
    POST - /api/v1/levels
    GET - /api/v1/levels/<int:page_size>/<int:page_num>
    GET - /api/v1/levels/<level_id>
    DELETE - /api/v1/levels/<level_id>
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
        
    def setUp(self) -> None:
        """
        Create levels before executing each test method.
        """
        self.levels = levels_data
        self.level_ids: list[str] = []

        for level in self.levels:
            self.response = self.client.post(
                "/api/v1/levels",
                json=level
            )
            self.level_ids.append(self.response.get_json().get("id"))

    def tearDown(self) -> None:
        """
        Delete the levels created after executing each test method.
        """
        for level_id in self.level_ids:
            self.client.delete(
                f"/api/v1/levels/{level_id}"
            )
        if storage.count(Level):
            raise ValueError("Levels deletion was not successful.")
    
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

    def test_add_level(self):
        """
        Test that level is created successfully.
        """
        self.assertEqual(self.response.status_code, 201)
        self.assertIn("name", self.response.get_json())
    
    def test_get_all_levels(self):
        """
        Test that all levels are retrieved from the database
        """
        response = self.client.get("/api/v1/levels")
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.get_json()), len(self.levels))
    
    def test_get_all_levels_with_pagination(self):
        """
        Test that levels are returned with pagination.
        """
        response = self.client.get(
            "/api/v1/levels",
            query_string={"page_size": 2, "page_num": 1}
        )
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.get_json()), 2)
    
    def test_get_level(self):
        """
        Test that a level is retrieved by its id.
        Verify that __class__ is not in the response.
        """
        response = self.client.get(f"/api/v1/levels/{self.level_ids[0]}")

        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.get_json())
        self.assertIn("no_of_courses_in_level", response.get_json())
        self.assertIn("no_of_users_in_level", response.get_json())
        self.assertNotIn("__class__", response.get_json())


if __name__ == "__main__":
    unittest.main(verbosity=2)
