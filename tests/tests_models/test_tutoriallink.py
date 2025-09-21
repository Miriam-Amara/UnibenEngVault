#!/usr/bin/env python3

"""
This module contains unittest for TutorialLink class
"""

from copy import deepcopy
from typing import Any
import json
import logging
import unittest

from models import storage
from models.basemodel import BaseModel
from models.course import Course
from models.level import Level
from models.tutoriallink import TutorialLink


logger = logging.getLogger(__name__)


class TestTutorialLink(unittest.TestCase):
    """
    Implements test cases for TutorialLink class.
    """

    def setUp(self) -> None:
        """
        """
        self.level = Level(name=100)
        self.level.save()
        course_data: dict[str, Any] = {
            "course_code": "IDE551",
            "semester": "first",
            "credit_load": 3,
            "title": "Computer Programming",
            "outline": "Programming in visual basic",
            "level_id": self.level.id,
        }
        self.course = Course(**course_data)
        self.course.save()

        tutorial_link_data: dict[str, Any] = {
            "course_id": self.course.id,
            "url": "https://youtube.com",
            "title": "dynamo",
            "content_type": "video",
            "level_id": self.level.id,
        }
        self.tutoriallink = TutorialLink(**tutorial_link_data)
        self.tutoriallink.save()

    def tearDown(self) -> None:
        """
        """
        self.level.delete()
        self.course.delete()
        self.tutoriallink.delete()
        storage.save()

    def test_instance_type(self):
        """
        Test that object of TutorialLink is an instance of
        TutorialLink and BaseModel.
        """
        self.assertIsInstance(self.tutoriallink, TutorialLink)
        self.assertIsInstance(self.tutoriallink, BaseModel)

    def test_instance_attributes(self):
        """
        Test that TutorialLink class has instance attributes
        from BaseModel (parent) class.
        """
        self.assertIn("id", self.tutoriallink.__dict__)
        self.assertIn("created_at", self.tutoriallink.__dict__)
        self.assertIn("updated_at", self.tutoriallink.__dict__)

    def test_class_attributes(self):
        """
        """
        self.assertIn("course_id", TutorialLink.__dict__)
        self.assertIn("url", TutorialLink.__dict__)
        self.assertIn("title", TutorialLink.__dict__)
        self.assertIn("content_type", TutorialLink.__dict__)
        self.assertIn("status", TutorialLink.__dict__)
        self.assertIn("level_id", TutorialLink.__dict__)
        self.assertIn("user_id", TutorialLink.__dict__)
        self.assertIn("admin_id", TutorialLink.__dict__)
        self.assertIn("added_by", TutorialLink.__dict__)
        self.assertIn("approved_by", TutorialLink.__dict__)

    def test_str_method(self):
        """
        """
        tutorial_link_dict = deepcopy(self.tutoriallink.__dict__)
        tutorial_link_dict.pop("_sa_instance_state")
        str_return_value = (
            f"[{self.tutoriallink.__class__.__name__}.{self.tutoriallink.id}] "
            f"({tutorial_link_dict})"
        )
        self.assertEqual(str_return_value, str(self.tutoriallink))
        logger.info(f"{str(self.tutoriallink)}")

    def test_save_method(self):
        """
        Tests that instance of TutorialLink class is saved to storage.
        """
        tutorial_link_count = storage.count(cls="TutorialLink")
        self.assertEqual(tutorial_link_count, 1)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of TutorialLink object.
        """
        tutorial_link_dict = self.tutoriallink.to_dict(
            include_relationships=True
        )
        self.assertIsInstance(tutorial_link_dict, dict)

        json.dumps(tutorial_link_dict)
        logger.info(f"{tutorial_link_dict}")


if __name__=="__main__":
    unittest.main(verbosity=2)
