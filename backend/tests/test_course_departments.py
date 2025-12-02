#!/usr/bin/env python3

"""
Implements test cases for combination
of courses and departments routes.
"""


from flask import Flask
from flask.testing import FlaskClient
from typing import cast
import logging
import unittest

from api.v1.app import create_app
from models import storage
from models.course import Course
from models.department import Department
from models.level import Level
from models.user import User
from tests.requests_data import (
    courses_data, departments_data, levels_data
)


logger = logging.getLogger(__name__)


class TestCourseDepartmentRoute(unittest.TestCase):
    """
    POST - /api/v1/courses/<course_id>/departments/<department_id>
    POST - /api/v1/departments/<department_id>/courses/<course_id>
    GET - /api/v1/departments/<department_id>/levels/<level_id>/courses
    DELETE - /api/v1/courses/<course_id>/departments/<department_id>
    DELETE - /api/v1/departments/<department_id>/courses/<course_id>
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

    def register_levels(self) -> None:
        """
        Create new levels.
        """
        self.levels = levels_data
        self.level_ids: list[str] = []

        for level in self.levels:
            response = self.client.post("/api/v1/levels", json=level)
            self.level_ids.append(response.get_json().get("id"))

    def register_departments(self) -> None:
        """
        Create new departments.
        """
        self.departments = departments_data
        self.dept_ids: list[str] = []

        for dept in self.departments:
            response = self.client.post("/api/v1/departments", json=dept)
            self.dept_ids.append(response.get_json().get("id"))

    def register_courses(self) -> None:
        """
        Creates new courses.
        """
        self.register_levels()
        self.courses = courses_data
        self.course_ids: list[str] = []

        for index, course in enumerate(self.courses):
            course["level_id"] = self.level_ids[index]
            self.response = self.client.post(
                "/api/v1/courses",
                json=course
            )
            self.course_ids.append(self.response.get_json().get("id"))

    def delete_courses(self):
        """
        Delete the created courses.
        """
        for course_id in self.course_ids:
            self.client.delete(f"/api/v1/courses/{course_id}")

    def delete_departments(self) -> None:
        """
        Delete the created departmnets.
        """
        for dept_id in self.dept_ids:
            self.client.delete(f"/api/v1/departments/{dept_id}")

    def delete_levels(self) -> None:
        """
        Delete the created levels
        """
        for level_id in self.level_ids:
            self.client.delete(f"/api/v1/levels/{level_id}")

    def setUp(self) -> None:
        """
        Adds courses to departments and departments to courses
        before each test method execution.
        """
        self.register_courses()
        self.register_departments()

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
        Delete the created courses, departments and levels
        after each test method execution.
        """
        self.delete_courses()
        self.delete_departments()
        self.delete_levels()

        if storage.count(Course):
            raise ValueError("Courses deletion was not successful.")
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

    def test_add_departments_to_course(self):
        """
        Test that departments are successfully addded to a course
        """
        for course_id in self.course_ids:
            for dept_id in self.dept_ids:
                response = self.client.post(
                    f"/api/v1/courses/{course_id}/departments/{dept_id}"
                )
                self.assertEqual(response.status_code, 201)

    def test_add_courses_to_department(self):
        """
        Test that courses are successfully added to a department.
        """
        for dept_id in self.dept_ids:
            for course_id in self.course_ids:
                response = self.client.post(
                    f"/api/v1/departments/{dept_id}/courses/{course_id}"
                )
                self.assertEqual(response.status_code, 201)

    def test_get_courses_by_department_and_level(self):
        """
        Test the retrieval of courses offered by a specific department
        and level and optionally filter by semester.
        """
        response = self.client.get(
            f"/api/v1/departments/{self.dept_ids[0]}"
            f"/levels/{self.level_ids[0]}/courses?semester=first"
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_department_from_course(self):
        """
        Tests that a department is successfully removed from a course.
        """
        department = cast(
            Department, storage.get_obj_by_id(Department, self.dept_ids[0])
        ).dept_name

        self.assertIn(
            department,
            self.client.get(f"/api/v1/courses/{self.course_ids[0]}")
            .get_json()
            .get("departments"),
        )

        response = self.client.delete(
            f"/api/v1/courses/{self.course_ids[0]}"
            f"/departments/{self.dept_ids[0]}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            department,
            response.get_json().get("departments")
        )

    def test_delete_course_from_department(self):
        """
        Test that a course is successfully removed from a department.
        """
        department = cast(
            Department, storage.get_obj_by_id(
                Department, self.dept_ids[0]
            )
        ).dept_name

        self.assertIn(
            department,
            self.client.get(f"/api/v1/courses/{self.course_ids[0]}")
            .get_json()
            .get("departments"),
        )

        response = self.client.delete(
            f"/api/v1/departments/{self.dept_ids[0]}"
            f"/courses/{self.course_ids[0]}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            department,
            response.get_json().get("departments")
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
