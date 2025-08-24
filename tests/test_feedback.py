#!/usr/bin/env python3

"""
This module contains unittest for Feedback class
"""

from copy import deepcopy
from dotenv import load_dotenv
from typing import Any
import json
import logging
import os
import unittest

from models.feedback import Feedback
from models.basemodel import BaseModel


load_dotenv()


class TestFeedback(unittest.TestCase):
    """
    Implements test cases for Feedback class.
    """

    def setUp(self) -> None:
        self.feedback = Feedback()
        self.feedback.save()

        self.feedback_objects: dict[str, Any] = {}
        self.filepath: str = os.getenv("FILE_PATH", "storage.json")
        try:
            with open(self.filepath, "r") as f:
                self.feedback_objects = json.load(f)
        except Exception as e:
            logging.debug(f"{e}")

    def tearDown(self) -> None:
        self.feedback.delete()
        self.feedback.save()

    def test_instance_type(self):
        """
        Test that object of Feedback is an instance of Feedback and BaseModel.
        """
        self.assertIsInstance(self.feedback, Feedback)
        self.assertIsInstance(self.feedback, BaseModel)

    def test_instance_attributes(self):
        """
        Test that Feedback class has instance attributes
        from BaseModel (parent) class.
        """
        self.assertIn("id", self.feedback.__dict__)
        self.assertIn("created_at", self.feedback.__dict__)
        self.assertIn("updated_at", self.feedback.__dict__)

    def test_class_attributes(self):
        self.assertIn("message", Feedback.__dict__)
        self.assertIn("status", Feedback.__dict__)
        self.assertIn("added_by", Feedback.__dict__)
        self.assertIn("reviewed_by", Feedback.__dict__)

    def test_str_method(self):
        return_value = (
            f"[{self.feedback.__class__.__name__}.{self.feedback.id}] "
            f"({self.feedback.__dict__})"
        )
        self.assertEqual(return_value, str(self.feedback))

    def test_save_method(self):
        """
        Tests that instance of Feedback class is saved to storage.
        """
        key = f"{self.feedback.__class__.__name__}.{self.feedback.id}"
        self.assertIn(key, self.feedback_objects)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Feedback object.
        """
        feedback_dict = deepcopy(self.feedback.__dict__)
        feedback_dict["created_at"] = self.feedback.created_at.isoformat()
        feedback_dict["updated_at"] = self.feedback.updated_at.isoformat()
        feedback_dict["__class__"] = self.feedback.__class__.__name__
        feedback_dict.pop("_sa_instance_state", None)
        self.assertEqual(feedback_dict, self.feedback.to_dict())
