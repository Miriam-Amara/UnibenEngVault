#!/usr/bin/env python3

"""
Defines the BaseModel class for all SQLAlchemy models in the system.
"""

from uuid import uuid4
from copy import deepcopy
from datetime import datetime
from enum import Enum
from typing import Any, cast
from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.inspection import inspect
import logging


logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class BaseModel:
    """
    A base class for creating UnibenEngVault models,
    providing common attributes and methods.
    """

    id = mapped_column(
        String(36), primary_key=True, nullable=False, sort_order=-3
    )
    created_at = mapped_column(
        DateTime, nullable=False, default=datetime.now, sort_order=-2
    )
    updated_at = mapped_column(
        DateTime, nullable=False, default=datetime.now, sort_order=-1
    )

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize a new instance with a unique ID and timestamps.

        Attributes:
            id (str): Generated using uuid4.
            created_at (datetime): Set to the current datetime at creation.
            updated_at (datetime): Set to the current datetime at creation.
        Additional attributes can be set via kwargs.
        """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        kwargs.pop("id", None)
        kwargs.pop("created_at", None)
        kwargs.pop("updated_at", None)
        self.__dict__.update(kwargs)
        from models import storage
        storage.new(self)

    def __str__(self) -> str:
        """Return a string representation of the model instance."""
        obj_dict = deepcopy(self.__dict__)
        obj_dict.pop("_sa_instance_state", None)
        obj_dict.pop("password", None)
        return f"[{self.__class__.__name__}.{self.id}] ({obj_dict})"

    def delete(self) -> None:
        """Delete the current instance from storage."""
        from models import storage
        storage.delete(self)

    def save(self) -> None:
        """Update 'updated_at' and save the instance to storage."""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def normalize_enums(self, obj_dict: dict[str, Any]) -> dict[str, Any]:
        """
        """
        for attr, value in obj_dict.items():
            if isinstance(value, Enum):
                obj_dict[attr] = value.value
            elif isinstance(value, list):
                obj_dict[attr] = [
                    {
                        k: (v.value if isinstance(v, Enum) else v)
                        for k, v in cast(dict[str, Any], item).items()
                    }
                    if isinstance(item, dict) else item
                    for item in value # type: ignore
                ]
        return obj_dict

    def to_dict(self, include_relationships: bool=False) -> dict[str, Any]:
        """
        Return a dictionary representation of the instance
        with datetimes as strings.
        """
        obj_dict = deepcopy(self.__dict__)

        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        obj_dict["__class__"] = self.__class__.__name__

        obj_dict.pop("_sa_instance_state", None)
        obj_dict.pop("password", None)

        if include_relationships:
            mapper = inspect(self.__class__)
            logger.debug(f"mapper: {mapper}")
            for rel in mapper.relationships: # type: ignore
                logger.debug(f"rel: {rel}")
                value = getattr(self, rel.key)
                logger.debug(f"value: {value}")
                if value is None:
                    obj_dict[rel.key] = None
                elif rel.uselist:
                    obj_dict[rel.key] = [v.to_dict() for v in value]
                else:
                    obj_dict[rel.key] = value.to_dict()
        
        return self.normalize_enums(obj_dict)
