#!/usr/bin/env python3

"""
This module contains BaseModel class for UnibenEngVault.
"""

from uuid import uuid4
from copy import deepcopy
from datetime import datetime
from typing import Any


class BaseModel:
    """
    Implements BaseModel class that is inherited by other classes.
    """
    def __init__(self, **kwargs: Any) -> None:
        if "__class__" in kwargs:
            kwargs["created_at"] = datetime.fromisoformat(kwargs["created_at"])
            kwargs["updated_at"] = datetime.fromisoformat(kwargs["updated_at"])
            kwargs.pop("__class__")
            self.__dict__.update(kwargs)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.__dict__.update(kwargs)
            from models import storage
            storage.new(self)
    
    def __str__(self) -> str:
        obj_dict = deepcopy(self.__dict__)
        obj_dict.pop("_sa_instance_state", None)
        return f"[{self.__class__.__name__}.{self.id}] ({obj_dict})"
        
    def delete(self) -> None:
        from models import storage
        storage.delete(self)

    def save(self) -> None:
        self.updated_at = datetime.now()
        from models import storage
        storage.save()

    def to_dict(self) -> dict[str, Any]:
        obj_dict = deepcopy(self.__dict__)
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict.pop("_sa_instance_state", None)
        return obj_dict
