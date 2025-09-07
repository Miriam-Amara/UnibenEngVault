#!usr/bin/env python3

"""
Database storage engine for managing ORM operations with SQLAlchemy.
"""

from dotenv import load_dotenv
from typing import Any, Optional
from sqlalchemy import Engine, create_engine, select, func
from sqlalchemy.orm import Session, sessionmaker, scoped_session
import os
import logging

from models.basemodel import BaseModel, Base
from models.admin import Admin, Permission, AdminPermission
from models.course import Course
from models.department import Department
from models.feedback import Feedback
from models.file import File
from models.help import Help
from models.level import Level
from models.notification import Notification
from models.report import Report
from models.tutoriallink import TutorialLink
from models.user import User
from models.department_level_courses import DepartmentLevelCourses

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


class DBStorage:
    """Manages database interactions using SQLAlchemy ORM."""

    __engine: Optional[Engine] = None
    __session: Optional[scoped_session[Session]] = None
    __user = os.getenv("UNIBENENGVAULT_POSTGRES_USER")
    __password = os.getenv("UNIBENENGVAULT_POSTGRES_PWD")
    __host = os.getenv("UNIBENENGVAULT_POSTGRES_HOST")
    __port = os.getenv("UNIBENENGVAULT_POSTGRES_PORT")
    __db = os.getenv("UNIBENENGVAULT_POSTGRES_DB")
    __classes: dict[str, Any] = {
        "Admin": Admin,
        "Permission": Permission,
        "AdminPermission": AdminPermission,
        "Course": Course,
        "Department": Department,
        "Feedback": Feedback,
        "File": File,
        "Help": Help,
        "Level": Level,
        "Notification": Notification,
        "Report": Report,
        "TutorialLink": TutorialLink,
        "User": User,
        "DepartmentLevelCourses": DepartmentLevelCourses
    }

    def __init__(self) -> None:
        """Initialize the database engine."""
        self.__url = (
            f"postgresql+psycopg2://{self.__user}:{self.__password}"
            f"@{self.__host}:{self.__port}/{self.__db}"
        )
        self.__engine = create_engine(
            self.__url, pool_pre_ping=True, echo=False
        )

    def all(
        self, page_size: int, page_num: int, cls: Optional[str] = None
    ) -> Optional[Any]:
        """Return all objects or objects of a given class with pagination."""
        assert self.__session is not None, "Session has not been initialized"

        if page_size <= 0:
            raise ValueError(f"{page_size} should be greater than zero")
        if not isinstance(page_size, int):  # type: ignore
            raise TypeError(f"{page_size} should be a valid integer.")
        if page_num <= 0:
            raise ValueError(f"{page_num} should be greater than zero")
        if not isinstance(page_num, int):  # type: ignore
            raise TypeError(f"{page_num} should be a valid integer.")
        assert self.__session is not None, "Session has not been initialized"

        if cls in self.__classes:
            cls_objects = self.__session.scalars(
                select(self.__classes[cls])
                .offset((page_num - 1) * page_size)
                .limit(page_size)
            )
            return cls_objects

        all_objects: list[Any] = []
        for cls_name in self.__classes.values():
            cls_objects = (
                self.__session.scalars(
                    select(cls_name)
                    .offset((page_num - 1) * page_size)
                    .limit(page_size)
                )
            ).all()
            all_objects.extend(cls_objects)
        return all_objects

    def close(self) -> None:
        """Close the current database session."""
        assert self.__session is not None, "Session has not been initialized"
        try:
            self.__session.close()
        except Exception as e:
            logger.error(f"DB operation failed: {e}")
            raise

    def count(self, cls: Optional[str] = None) -> int | dict[str, int] | None:
        """
        Return the total number of objects of a class
        or all classes in storage.
        """
        assert self.__session is not None, "Session has not been initialized"

        if cls in self.__classes:
            cls_objects_count = self.__session.scalar(
                select(func.count()).select_from(self.__classes[cls])
            )
            return cls_objects_count

        all_obj_count: dict[str, int] = {}
        for cls_name in self.__classes.values():
            cls_objects_count = self.__session.scalar(
                select(func.count()).select_from(cls_name)
            )
            if cls_objects_count:
                all_obj_count[cls_name] = cls_objects_count
        return all_obj_count

    def delete(self, obj: BaseModel) -> None:
        """Delete an object from the current session."""
        assert self.__session is not None, "Session has not been initialized"
        try:
            self.__session.delete(obj)
        except Exception as e:
            logger.error(f"DB operation failed: {e}")
            raise
    
    def get(self, cls: str, id: str) -> Optional[BaseModel]:
        """
        Returns the object based on the class and its ID, or None if not found.
        """
        assert self.__session is not None, "Session has not been initialized"
        if cls not in self.__classes:
            return
        if not isinstance(id, str): # type: ignore
            return
        
        obj = self.__session.scalars(
            select(self.__classes[cls]).where(self.__classes[cls].id == id)
        ).one_or_none()
        return obj

    def new(self, obj: BaseModel) -> Optional[str]:
        """Add a new object to the current session."""
        assert self.__session is not None, "Session has not been initialized"
        try:
            self.__session.add(obj)
            return obj.id
        except Exception as e:
            logger.error(f"DB operation failed: {e}")
            raise

    def save(self) -> None:
        """Commit the current transaction, rollback if an error occurs."""
        assert self.__session is not None, "Session has not been initialized"
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            logger.error(f"DB operation failed: {e}")
            raise

    def reload(self) -> None:
        """Create database tables and initialize the session factory."""
        assert self.__engine is not None, "Engine has not been initialized"
        try:
            Base.metadata.create_all(self.__engine)
        except Exception as e:
            logger.critical(f"DB table creation failed: {e}")
            raise

        self.__session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )
