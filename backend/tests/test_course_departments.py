#!/usr/bin/env python3

"""

"""


from flask import Flask
from flask.testing import FlaskClient
import logging
import unittest

from api.v1.app import create_app
from models import storage
from models.course import Course
from models.department import Department
from models.level import Level
from models.user import User
from tests.requests_data import course_data, department_data, level_data


logger = logging.getLogger(__name__)


class TestCourseDepartmentRoute(unittest.TestCase):
    """
    POST - /api/v1/courses/<course_id>/departments/<department_id>
    POST - /api/v1/departments/<department_id>/courses/<course_id>
    GET - /api/v1/courses/<course_id>/departments
    GET - /api/v1/departments/<department_id>/levels/<level_id>/courses
    DELETE - /api/v1/courses/<course_id>/departments/<department_id>
    DELETE - /api/v1/departments/<department_id>/courses/<course_id>
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
    
    def delete_courses(self):
        """
        """
        for course_id in self.course_ids:
            self.client.delete(
                f"/api/v1/courses/{course_id}"
            )

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
        self.add_courses()
        self.add_departments()
        for course_id in self.course_ids:
            for dept_id in self.dept_ids:
                self.client.post(
                    f"/api/v1/courses/{course_id}/departments/{dept_id}"
                )
        
        for dept_id in self.dept_ids:
            for course_id in self.course_ids:
                self.client.post(
                    f"/api/v1/departments/{dept_id}/courses/{course_id}"
                )
        
        
    def tearDown(self) -> None:
        """
        """
        self.delete_courses()
        self.delete_department()
        self.delete_level()

        if storage.count(Course):
            raise ValueError("Courses deletion was not successful.")
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
    
    def test_add_course_departments(self):
        """
        """
        for course_id in self.course_ids:
            for dept_id in self.dept_ids:
                response = self.client.post(
                    f"/api/v1/courses/{course_id}/departments/{dept_id}"
                )
                self.assertEqual(response.status_code, 201)
    
    def test_add_department_courses(self):
        """
        """
        for dept_id in self.dept_ids:
            for course_id in self.course_ids:
                response = self.client.post(
                    f"/api/v1/departments/{dept_id}/courses/{course_id}"
                )
                self.assertEqual(response.status_code, 201)

    def test_get_course_departments(self):
        """
        """
        response = self.client.get(
            f"/api/v1/courses/{self.course_ids[0]}/departments"
        )
        self.assertEqual(response.status_code, 200)
        
    def test_get_department_level_courses(self):
        """
        """
        response = self.client.get(
            f"/api/v1/departments/{self.dept_ids[0]}"
            f"/levels/{self.level_ids[0]}/courses?semester=first"
        )
        self.assertEqual(response.status_code, 200)
        import json
        logger.debug(json.dumps(response.get_json(), indent=4))

    def test_delete_course_department(self):
        """
        """
        pass

    def test_delete_department_course(self):
        """
        """
        pass
  

if __name__ == "__main__":
    unittest.main(verbosity=2)
