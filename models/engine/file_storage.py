#!usr/bin/env python3

"""
This module contains FileStorage class for storing objects
in json file.
"""

from dotenv import load_dotenv
from typing import Any, Optional
import json
import os

load_dotenv()

from models.basemodel import BaseModel


class FileStorage:
    __objects: dict[str, Any] = {}
    __filestorage: str = os.getenv("FILE_PATH", "storage.json")
    __classes = {
        "BaseModel": BaseModel,
    }

    def all(self, cls: Optional[str]) -> dict[str, Any]:
        if cls in self.__classes:
            cls_objects = {
                cls_id: obj for cls_id, obj in self.__objects.items() if cls in cls_id
                }
            return cls_objects
        return self.__objects
    
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
