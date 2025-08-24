#!/usr/bin/env python3

"""
This module contains unittest for Department class
"""

from copy import deepcopy
from dotenv import load_dotenv
from typing import Any
import json
import logging
import os
import unittest

from models.department import Department
from models.basemodel import BaseModel


load_dotenv()


class TestDepartment(unittest.TestCase):
    """
    Implements test cases for Department class.
    """

    def setUp(self) -> None:
        self.department = Department()
        self.department.save()

        self.department_objects: dict[str, Any] = {}
        self.filepath: str = os.getenv("FILE_PATH", "storage.json")
        try:
            with open(self.filepath, "r") as f:
                self.department_objects = json.load(f)
        except Exception as e:
            logging.debug(f"{e}")

    def tearDown(self) -> None:
        self.department.delete()
        self.department.save()

    def test_instance_type(self):
        """
        Test that object of Department is an instance of
        Department and BaseModel.
        """
        self.assertIsInstance(self.department, Department)
        self.assertIsInstance(self.department, BaseModel)

    def test_instance_attributes(self):
        """
        Test that Department class has instance attributes
        from BaseModel (parent) class.
        """
        self.assertIn("id", self.department.__dict__)
        self.assertIn("created_at", self.department.__dict__)
        self.assertIn("updated_at", self.department.__dict__)

    def test_class_attributes(self):
        self.assertIn("name", Department.__dict__)
        self.assertIn("code", Department.__dict__)
        self.assertIn("course_assignments", Department.__dict__)
        self.assertIn("registered_by", Department.__dict__)

    def test_str_method(self):
        return_value = (
            f"[{self.department.__class__.__name__}.{self.department.id}] "
            f"({self.department.__dict__})"
        )
        self.assertEqual(return_value, str(self.department))

    def test_save_method(self):
        """
        Tests that instance of Department class is saved to storage.
        """
        key = f"{self.department.__class__.__name__}.{self.department.id}"
        self.assertIn(key, self.department_objects)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Department object.
        """
        department_dict = deepcopy(self.department.__dict__)
        department_dict["created_at"] = self.department.created_at.isoformat()
        department_dict["updated_at"] = self.department.updated_at.isoformat()
        department_dict["__class__"] = self.department.__class__.__name__
        department_dict.pop("_sa_instance_state", None)
        self.assertEqual(department_dict, self.department.to_dict())
