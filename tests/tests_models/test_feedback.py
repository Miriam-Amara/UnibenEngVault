#!/usr/bin/env python3

"""
This module contains unittest for Feedback class
"""

from copy import deepcopy
import json
import logging
import unittest

from models import storage
from models.basemodel import BaseModel
from models.department import Department
from models.feedback import Feedback
from models.level import Level
from models.user import User


logger = logging.getLogger(__name__)


class TestFeedback(unittest.TestCase):
    """
    Implements test cases for Feedback class.
    """

    def setUp(self) -> None:
        """
        """
        self.department = Department(dept_name="electrical engineering", dept_code="eee")
        self.level = Level(name=100)
        self.user = User(
            email="user2@gmail.com", password="345",
            department_id=self.department.id, level_id=self.level.id 
        )
        storage.save()

        self.feedback = Feedback(
            message="UnibenEngVault is the best",
            user_id=self.user.id
        )
        self.feedback.save()

    def tearDown(self) -> None:
        """
        """
        self.department.delete()
        self.level.delete()
        self.user.delete()
        self.feedback.delete()
        storage.save()

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
        """
        """
        self.assertIn("message", Feedback.__dict__)
        self.assertIn("status", Feedback.__dict__)
        self.assertIn("user_id", Feedback.__dict__)
        self.assertIn("admin_id", Feedback.__dict__)
        self.assertIn("added_by", Feedback.__dict__)
        self.assertIn("reviewed_by", Feedback.__dict__)

    def test_str_method(self):
        """
        """
        feedback_dict = deepcopy(self.feedback.__dict__)
        feedback_dict.pop("_sa_instance_state", None)
        str_return_value = (
            f"[{self.feedback.__class__.__name__}.{self.feedback.id}] "
            f"({feedback_dict})"
        )
        self.assertEqual(str_return_value, str(self.feedback))
        logger.info(f"{str(self.feedback)}")

    def test_save_method(self):
        """
        Tests that instance of Feedback class is saved to storage.
        """
        feedback_count = storage.count(cls="Feedback")
        self.assertEqual(feedback_count, 1)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Feedback object.
        """
        feedback_dict = self.feedback.to_dict(include_relationships=True)
        self.assertIsInstance(feedback_dict, dict)

        json.dumps(feedback_dict)
        logger.info(f"{feedback_dict}")


if __name__=="__main__":
    unittest.main(verbosity=2)
