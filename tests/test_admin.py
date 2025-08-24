#!/usr/bin/env python3

"""
This module contains unittest for Admin class
"""

from copy import deepcopy
from dotenv import load_dotenv
from typing import Any
import json
import logging
import os
import unittest

from models.admin import Admin
from models.basemodel import BaseModel


load_dotenv()


class TestAdmin(unittest.TestCase):
    """
    Implements test cases for Admin class.
    """

    def setUp(self) -> None:
        self.admin = Admin()
        self.admin.save()

        self.admin_objects: dict[str, Any] = {}
        self.filepath: str = os.getenv("FILE_PATH", "storage.json")
        try:
            with open(self.filepath, "r") as f:
                self.admin_objects = json.load(f)
        except Exception as e:
            logging.debug(f"{e}")

    def tearDown(self) -> None:
        self.admin.delete()
        self.admin.save()

    def test_instance_type(self):
        """
        Test that object of Admin is an instance of Admin and BaseModel.
        """
        self.assertIsInstance(self.admin, Admin)
        self.assertIsInstance(self.admin, BaseModel)

    def test_instance_attributes(self):
        """
        Test that Admin class has instance attributes from BaseModel (parent)
        class.
        """
        self.assertIn("id", self.admin.__dict__)
        self.assertIn("created_at", self.admin.__dict__)
        self.assertIn("updated_at", self.admin.__dict__)

    def test_class_attributes(self):
        self.assertIn("is_super_admin", Admin.__dict__)
        self.assertIn("user", Admin.__dict__)
        self.assertIn("admin_permissions", Admin.__dict__)

    def test_str_method(self):
        return_value = (
            f"[{self.admin.__class__.__name__}.{self.admin.id}] "
            f"({self.admin.__dict__})"
        )
        self.assertEqual(return_value, str(self.admin))

    def test_save_method(self):
        """
        Tests that instance of Admin class is saved to storage.
        """
        key = f"{self.admin.__class__.__name__}.{self.admin.id}"
        self.assertIn(key, self.admin_objects)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Admin object.
        """
        admin_dict = deepcopy(self.admin.__dict__)
        admin_dict["created_at"] = self.admin.created_at.isoformat()
        admin_dict["updated_at"] = self.admin.updated_at.isoformat()
        admin_dict["__class__"] = self.admin.__class__.__name__
        admin_dict.pop("_sa_instance_state", None)
        self.assertEqual(admin_dict, self.admin.to_dict())
