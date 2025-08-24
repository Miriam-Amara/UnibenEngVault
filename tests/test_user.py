#!/usr/bin/env python3

"""
This module contains unittest for User class
"""

from copy import deepcopy
from dotenv import load_dotenv
from typing import Any
import json
import logging
import os
import unittest

from models.user import User
from models.basemodel import BaseModel


load_dotenv()


class TestUser(unittest.TestCase):
    """
    Implements test cases for User class.
    """

    def setUp(self) -> None:
        self.user = User()
        self.user.save()

        self.user_objects: dict[str, Any] = {}
        self.filepath: str = os.getenv("FILE_PATH", "storage.json")
        try:
            with open(self.filepath, "r") as f:
                self.user_objects = json.load(f)
        except Exception as e:
            logging.debug(f"{e}")

    def tearDown(self) -> None:
        self.user.delete()
        self.user.save()

    def test_instance_type(self):
        """
        Test that object of User is an instance of User and BaseModel.
        """
        self.assertIsInstance(self.user, User)
        self.assertIsInstance(self.user, BaseModel)

    def test_instance_attributes(self):
        """
        Test that User class has instance attributes from BaseModel (parent)
        class.
        """
        self.assertIn("id", self.user.__dict__)
        self.assertIn("created_at", self.user.__dict__)
        self.assertIn("updated_at", self.user.__dict__)

    def test_class_attributes(self):
        self.assertIn("email", User.__dict__)
        self.assertIn("password", User.__dict__)
        self.assertIn("department", User.__dict__)
        self.assertIn("level", User.__dict__)
        self.assertIn("role", User.__dict__)
        self.assertIn("is_active", User.__dict__)
        self.assertIn("warnings_count", User.__dict__)
        self.assertIn("suspensions_count", User.__dict__)

    def test_str_method(self):
        return_value = (
            f"[{self.user.__class__.__name__}.{self.user.id}] "
            f"({self.user.__dict__})"
        )
        self.assertEqual(return_value, str(self.user))

    def test_save_method(self):
        """
        Tests that instance of User class is saved to storage.
        """
        key = f"{self.user.__class__.__name__}.{self.user.id}"
        self.assertIn(key, self.user_objects)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of User object.
        """
        user_dict = deepcopy(self.user.__dict__)
        user_dict["created_at"] = self.user.created_at.isoformat()
        user_dict["updated_at"] = self.user.updated_at.isoformat()
        user_dict["__class__"] = self.user.__class__.__name__
        user_dict.pop("_sa_instance_state", None)
        self.assertEqual(user_dict, self.user.to_dict())
