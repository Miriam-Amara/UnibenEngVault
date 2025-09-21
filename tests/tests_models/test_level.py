#!/usr/bin/env python3

"""
This module contains unittest for Level class
"""

from copy import deepcopy
import json
import logging
import unittest

from models import storage
from models.basemodel import BaseModel
from models.level import Level

logger = logging.getLogger(__name__)


class TestLevel(unittest.TestCase):
    """
    Implements test cases for Level class.
    """

    def setUp(self) -> None:
        """
        """
        self.level = Level(name=100)
        self.level.save()

    def tearDown(self) -> None:
        """
        """
        self.level.delete()
        storage.save()

    def test_instance_type(self):
        """
        Test that object of Level is an instance of Level and BaseModel.
        """
        self.assertIsInstance(self.level, Level)
        self.assertIsInstance(self.level, BaseModel)

    def test_instance_attributes(self):
        """
        Test that Level class has instance attributes from BaseModel (parent)
        class.
        """
        self.assertIn("id", self.level.__dict__)
        self.assertIn("created_at", self.level.__dict__)
        self.assertIn("updated_at", self.level.__dict__)

    def test_class_attributes(self):
        """
        """
        self.assertIn("name", Level.__dict__)
        self.assertIn("users", Level.__dict__)
        self.assertIn("courses", Level.__dict__)
        self.assertIn("admin_permissions", Level.__dict__)

    def test_str_method(self):
        """
        """
        level_dict = deepcopy(self.level.__dict__)
        level_dict.pop("_sa_instance_state")
        str_return_value = (
            f"[{self.level.__class__.__name__}.{self.level.id}] "
            f"({level_dict})"
        )
        self.assertEqual(str_return_value, str(self.level))
        logger.info(f"{str(level_dict)}")

    def test_save_method(self):
        """
        Tests that instance of Level class is saved to storage.
        """
        level_count = storage.count(cls="Level")
        self.assertEqual(level_count, 1)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Level object.
        """
        level_dict = self.level.to_dict(include_relationships=True)
        self.assertIsInstance(level_dict, dict)

        json.dumps(level_dict)
        logger.info(f"{level_dict}")


if __name__=="__main__":
    unittest.main(verbosity=2)
