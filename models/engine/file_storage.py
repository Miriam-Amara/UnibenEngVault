#!usr/bin/env python3

"""
This module contains FileStorage class for storing objects
in json file.
"""

from copy import deepcopy
from dotenv import load_dotenv
from typing import Any, Optional
import json
import os

load_dotenv()

from models.basemodel import BaseModel
from models.admin import Admin, Permission, AdminPermission
from models.course import Course, CourseAssignment
from models.department import Department
from models.faculty import Faculty
from models.feedback import Feedback
from models.file import File
from models.help import Help
from models.level import Level
from models.notification import Notification
from models.report import Report
from models.tutoriallink import TutorialLink
from models.user import User


class FileStorage:
    __objects: dict[str, Any] = {}
    __filestorage: str = os.getenv("FILE_PATH", "storage.json")
    __classes: dict[str, Any] = {
        "BaseModel": BaseModel,
        "Admin": Admin,
        "Permission": Permission,
        "AdminPermission": AdminPermission,
        "Course": Course,
        "CourseAssignment": CourseAssignment,
        "Department": Department,
        "Faculty": Faculty,
        "Feedback": Feedback,
        "File": File,
        "Help": Help,
        "Level": Level,
        "Notification": Notification,
        "Report": Report,
        "TutorialLink": TutorialLink,
        "User": User
    }

    def all(self, cls: Optional[str]=None) -> dict[str, Any]:
        objects = deepcopy(self.__objects)
        if cls in self.__classes:
            cls_objects = {
                cls_id: obj for cls_id, obj in self.__objects.items() if cls in cls_id
                }
            return cls_objects
        return objects
    
    def count(self, cls: Optional[str]=None) -> int:
        """
        Returns the total number of objects of a given class or
        total number of all objects in storage.
        """
        count = 0
        if cls not in self.__classes:
            for _ in self.__objects:
                count += 1
            return count
        
        for cls_id in self.__objects:
            if cls in cls_id:
                count += 1
        return count

    def delete(self, obj: BaseModel) -> None:
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects.pop(key, None)

    def new(self, obj: BaseModel) -> None:
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self) -> None:
        obj_dict = {
            cls_id: obj.to_dict() for cls_id, obj in self.__objects.items()
            }
        with open(self.__filestorage, "w", encoding="utf-8") as f:
            json.dump(obj_dict, f, indent=4) 

    def reload(self) -> None:
        all_objects: dict[str, Any] = {}
        try:
            with open(self.__filestorage, "r") as f:
                all_objects = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            pass

        for cls_id, obj_dict in all_objects.items():
            cls_name = self.__classes[obj_dict["__class__"]]
            self.__objects[cls_id] = cls_name(**obj_dict)
