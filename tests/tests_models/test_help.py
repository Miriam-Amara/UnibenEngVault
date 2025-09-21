#!/usr/bin/env python3

"""
This module contains unittest for Help class
"""

from copy import deepcopy
import json
import logging
import unittest

from models import storage
from models.basemodel import BaseModel
from models.help import Help


logger = logging.getLogger(__name__)


class TestHelp(unittest.TestCase):
    """
    Implements test cases for Help class.
    """

    def setUp(self) -> None:
        """
        """
        self.help = Help(help_type="academic", message="I can't find my courses.")
        self.help.save()

    def tearDown(self) -> None:
        """
        """
        self.help.delete()
        storage.save()

    def test_instance_type(self):
        """
        Test that object of Help is an instance of Help and BaseModel.
        """
        self.assertIsInstance(self.help, Help)
        self.assertIsInstance(self.help, BaseModel)

    def test_instance_attributes(self):
        """
        Test that Help class has instance attributes from BaseModel (parent)
        class.
        """
        self.assertIn("id", self.help.__dict__)
        self.assertIn("created_at", self.help.__dict__)
        self.assertIn("updated_at", self.help.__dict__)

    def test_class_attributes(self):
        """
        """
        self.assertIn("help_type", Help.__dict__)
        self.assertIn("message", Help.__dict__)
        self.assertIn("is_faq", Help.__dict__)
        self.assertIn("priority", Help.__dict__)
        self.assertIn("status", Help.__dict__)
        self.assertIn("response", Help.__dict__)
        self.assertIn("user_id", Help.__dict__)
        self.assertIn("admin_id", Help.__dict__)
        self.assertIn("added_by", Help.__dict__)
        self.assertIn("reviewed_by", Help.__dict__)

    def test_str_method(self):
        """
        """
        help_dict = deepcopy(self.help.__dict__)
        help_dict.pop("_sa_instance_state")
        str_return_value = (
            f"[{self.help.__class__.__name__}.{self.help.id}] ({help_dict})"
        )
        self.assertEqual(str_return_value, str(self.help))
        logger.info(f"{str(self.help)}")

    def test_save_method(self):
        """
        Tests that instance of Help class is saved to storage.
        """
        help_count = storage.count(cls="Help")
        self.assertEqual(help_count, 1)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Help object.
        """
        help_dict = self.help.to_dict(include_relationships=True)
        self.assertIsInstance(help_dict, dict)

        json.dumps(help_dict)
        logger.info(f"{help_dict}")


if __name__=="__main__":
    unittest.main(verbosity=2)
