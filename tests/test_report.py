#!/usr/bin/env python3

"""
This module contains unittest for Report class
"""

from copy import deepcopy
from dotenv import load_dotenv
from typing import Any
import json
import logging
import os
import unittest

from models.report import Report
from models.basemodel import BaseModel


load_dotenv()


class TestReport(unittest.TestCase):
    """
    Implements test cases for Report class.
    """

    def setUp(self) -> None:
        self.report = Report()
        self.report.save()

        self.report_objects: dict[str, Any] = {}
        self.filepath: str = os.getenv("FILE_PATH", "storage.json")
        try:
            with open(self.filepath, "r") as f:
                self.report_objects = json.load(f)
        except Exception as e:
            logging.debug(f"{e}")

    def tearDown(self) -> None:
        self.report.delete()
        self.report.save()

    def test_instance_type(self):
        """
        Test that object of Report is an instance of Report and BaseModel.
        """
        self.assertIsInstance(self.report, Report)
        self.assertIsInstance(self.report, BaseModel)

    def test_instance_attributes(self):
        """
        Test that Report class has instance attributes from BaseModel (parent)
        class.
        """
        self.assertIn("id", self.report.__dict__)
        self.assertIn("created_at", self.report.__dict__)
        self.assertIn("updated_at", self.report.__dict__)

    def test_class_attributes(self):
        self.assertIn("topic", Report.__dict__)
        self.assertIn("message", Report.__dict__)
        self.assertIn("priority", Report.__dict__)
        self.assertIn("status", Report.__dict__)
        self.assertIn("file", Report.__dict__)
        self.assertIn("tutorial_link", Report.__dict__)
        self.assertIn("reported_by", Report.__dict__)
        self.assertIn("response", Report.__dict__)
        self.assertIn("reviewed_by", Report.__dict__)

    def test_str_method(self):
        return_value = (
            f"[{self.report.__class__.__name__}.{self.report.id}] "
            f"({self.report.__dict__})"
        )
        self.assertEqual(return_value, str(self.report))

    def test_save_method(self):
        """
        Tests that instance of Report class is saved to storage.
        """
        key = f"{self.report.__class__.__name__}.{self.report.id}"
        self.assertIn(key, self.report_objects)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a serializable
        json object of Report object.
        """
        report_dict = deepcopy(self.report.__dict__)
        report_dict["created_at"] = self.report.created_at.isoformat()
        report_dict["updated_at"] = self.report.updated_at.isoformat()
        report_dict["__class__"] = self.report.__class__.__name__
        report_dict.pop("_sa_instance_state", None)
        self.assertEqual(report_dict, self.report.to_dict())
