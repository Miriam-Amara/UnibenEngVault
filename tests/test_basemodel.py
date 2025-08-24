#!/usr/bin/env python3

"""
This module contains unittest for BaseModel class
"""

from copy import deepcopy
from datetime import datetime
from dotenv import load_dotenv
from typing import Any
from uuid import UUID
import json
import logging
import os
import unittest

from models.basemodel import BaseModel


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
    filename="tests/tests.log",
)

disable_logging: bool = False
if disable_logging:
    logging.disable(logging.CRITICAL)

load_dotenv()


class TestBaseModel(unittest.TestCase):
    """
    Implements test cases for attributes and methods of BaseModel class.
    """

    def setUp(self) -> None:
        """
        Creates an object of BaseModel class for every test case.
        """
        self.basemodel: BaseModel = BaseModel()
        self.basemodel.save()

        self.objects: dict[str, Any] = {}
        self.filepath: str = os.getenv("FILE_PATH", "storage.json")
        try:
            with open(self.filepath, "r") as f:
                self.objects = json.load(f)
        except Exception as e:
            logging.debug(f"{e}")

    def tearDown(self) -> None:
        """
        Removes objects from storage.
        """
        self.basemodel.delete()
        self.basemodel.save()

    def test_instance_attributes(self):
        """
        Test presence of instance attributes
        """
        self.assertIn("id", self.basemodel.__dict__)
        self.assertIn("created_at", self.basemodel.__dict__)
        self.assertIn("updated_at", self.basemodel.__dict__)

    def test_instance_attributes_type(self):
        """
        Test the type of instance attributes
        """
        self.assertIsInstance(UUID(self.basemodel.id), UUID)
        self.assertIsInstance(self.basemodel.created_at, datetime)
        self.assertIsInstance(self.basemodel.updated_at, datetime)

    def test_instance_creation_with_args(self):
        new_basemodel = BaseModel(name="Peter", faculty="Engineering")
        self.assertIn("name", new_basemodel.__dict__)
        self.assertIn("faculty", new_basemodel.__dict__)
        new_basemodel.delete()

    def test_instance_recreation(self):
        """
        Test that a basemodel instance can be recreated.
        """
        obj_dict = deepcopy(self.basemodel.__dict__)
        new_basemodel = BaseModel(**obj_dict)
        self.assertEqual(new_basemodel.id, self.basemodel.id)
        self.assertEqual(new_basemodel.created_at, self.basemodel.created_at)
        self.assertEqual(new_basemodel.updated_at, self.basemodel.updated_at)

    def test_str_method(self):
        """
        Test that __str__ method returns a string representation
        of basemodel instance.
        """
        return_value = (
            f"[{self.basemodel.__class__.__name__}.{self.basemodel.id}] "
            f"({self.basemodel.__dict__})"
        )
        self.assertEqual(return_value, str(self.basemodel))

    def test_delete_method(self):
        """
        Tests that object is deleted from storage.
        """
        key = f"{self.basemodel.__class__.__name__}.{self.basemodel.id}"
        self.assertIn(key, self.objects)
        self.basemodel.delete()
        self.basemodel.save()

        self.objects: dict[str, Any] = {}
        self.filepath: str = os.getenv("FILE_PATH", "storage.json")
        try:
            with open(self.filepath, "r") as f:
                self.objects = json.load(f)
        except Exception as e:
            logging.debug(f"{e}")
        self.assertNotIn(key, self.objects)

    def test_save_method(self):
        """
        Tests that object of BaseModel is saved in storage.
        """
        key = f"{self.basemodel.__class__.__name__}.{self.basemodel.id}"
        self.assertIn(key, self.objects)

    def test_to_dict_method(self):
        basemodel_dict = deepcopy(self.basemodel.__dict__)
        basemodel_dict["created_at"] = self.basemodel.created_at.isoformat()
        basemodel_dict["updated_at"] = self.basemodel.updated_at.isoformat()
        basemodel_dict["__class__"] = self.basemodel.__class__.__name__
        basemodel_dict.pop("_sa_instance_state", None)
        self.assertEqual(basemodel_dict, self.basemodel.to_dict())
