#!usr/bin/env python3

"""
Database storage engine for managing ORM operations with SQLAlchemy.
"""

from datetime import datetime
from dotenv import load_dotenv
from typing import Any, Optional, Sequence, Type, TypeVar, cast
from sqlalchemy import create_engine, select, and_, func
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import Select
import logging

from models.basemodel import BaseModel, Base
from models.admin import Admin, Permission, AdminPermission
from models.course import (
    Course, Semester, course_departments  # type: ignore
)
from models.department import Department
from models.feedback import Feedback
from models.file import File
from models.help import Help
from models.level import Level
from models.notification import (
    Notification, notification_reads  # type: ignore
)
from models.report import Report
from models.tutoriallink import TutorialLink
from models.user import User
from models.user_session import UserSession


load_dotenv()
logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


class DBStorage:
    """Manages database interactions using SQLAlchemy ORM."""

    __classes: list[Type[BaseModel]] = [
        Admin,
        Permission,
        AdminPermission,
        Course,
        Department,
        Feedback,
        File,
        Help,
        Level,
        Notification,
        Report,
        TutorialLink,
        User,
        UserSession,
    ]

    def __init__(self, database_url: str) -> None:
        """Initialize the database engine."""
        self.__engine = create_engine(database_url, pool_pre_ping=True)

    def all(
        self,
        cls: Type[T],
        page_size: int | str | None = None,
        page_num: int | str | None = None,
    ) -> Sequence[T]:
        """
        Returns all objects of a class with optional pagination.
        """
        if not issubclass(cls, BaseModel):  # type: ignore
            raise TypeError("Cls must inherit from BaseModel")

        stmt = select(cls)

        if page_size and page_num:
            stmt = self.apply_pagination(stmt, page_size, page_num)

        return self.__session.scalars(stmt).all()

    def apply_pagination(
        self, stmt: Select[Any], page_size: str | int, page_num: str | int
    ):
        """
        Apply pagination if provided.
        """
        if page_size and page_num:
            try:
                page_size = int(page_size)
                page_num = int(page_num)
            except ValueError:
                raise ValueError(
                    "page_size and page_num must be positive integers"
                )

            stmt = stmt.offset((int(page_num) - 1) * int(page_size)).limit(
                int(page_size)
            )

        return stmt

    def close(self) -> None:
        """Close the current database session."""
        self.__session.close()

    def count(self, cls: Type[T] | None = None) -> int | dict[str, Any] | None:
        """
        Return the total number of objects of a class
        or all classes in storage.
        """
        if cls in self.__classes:
            cls_objects_count = self.__session.scalar(
                select(func.count()).select_from(cls)
            )
            return cls_objects_count

        all_obj_count: dict[str, Any] = {}
        for cls_name in self.__classes:
            cls_objects_count = self.__session.scalar(
                select(func.count()).select_from(cls_name)
            )
            all_obj_count[cls_name.__name__] = cls_objects_count
        return all_obj_count

    def delete(self, obj: BaseModel) -> None:
        """Delete an object from the current session."""
        self.__session.delete(obj)

    def filter(
        self,
        cls: Type[T],
        search_str: str | None = None,
        date_str: str | None = None,
        file_status: str | None = None,
        page_size: int | str | None = None,
        page_num: int | str | None = None,
    ) -> Sequence[T]:
        """
        Returns objects of a class filtered optionally by:
        - search str
        - date
        - file status
        - pagination
        """

        search_map: dict[Any, Any] = {
            Course: Course.course_code,
            User: User.email,
            File: File.file_name,
            Department: Department.dept_name,
            Level: Level.level_name,
        }

        if not issubclass(cls, BaseModel):  # type: ignore
            raise TypeError("Cls must inherit from BaseModel")

        if search_str and not isinstance(search_str, str):  # type: ignore
            raise ValueError("search_str must be a string")

        if file_status and not isinstance(file_status, str):  # type: ignore
            raise ValueError("file_status must be a string")

        stmt = select(cls)
        filters: list[Select[Any]] = []

        if search_str:
            column = cast(Any, search_map.get(cls))
            filters.append(column.ilike(f"%{search_str}%"))

        if file_status:
            filters.append(File.status == file_status)  # type: ignore

        if date_str:
            try:
                date_only = datetime.fromisoformat(date_str).date()
            except ValueError:
                raise ValueError("date_str must be a valid ISO datetime")
            filters.append(
                func.date(cls.created_at) == date_only  # type: ignore
            )

        if filters:
            stmt = stmt.where(*filters)  # type: ignore

        if page_size and page_num:
            stmt = self.apply_pagination(stmt, page_size, page_num)

        return self.__session.scalars(stmt).all()

    def get_obj_by_id(self, cls: Type[T], id: str) -> T | None:
        """
        Returns an object based on its class and  ID, or None if not found.
        """
        if issubclass(cls, BaseModel):  # type: ignore
            obj = self.__session.get(cls, id)
            return obj

    def get_users_by_dept_and_level(
        self,
        department_id: str,
        level_id: str,
        page_size: int | str | None = None,
        page_num: int | str | None = None,
    ) -> Sequence[User] | None:
        """
        Returns all users in a specific department and level.
        """
        if page_size and page_num:
            try:
                page_size = int(page_size)
                page_num = int(page_num)
            except ValueError:
                raise ValueError(
                    "page_size and page_num must be positive integers"
                )

        if (
            not isinstance(department_id, str)  # type: ignore
            or not isinstance(level_id, str)  # type: ignore
        ):
            raise ValueError("department_id and level_id must be a valid str.")

        stmt = (
            select(User)
            .where(
                and_(
                    User.department_id == department_id,
                    User.level_id == level_id
                )
            )
        )
        if page_size and page_num:
            stmt = (
                stmt
                .offset((int(page_num) - 1) * int(page_size))
                .limit(int(page_size))
            )
        user_objects = self.__session.scalars(stmt).all()
        return user_objects

    def get_courses_by_dept_and_level(
        self, department_id: str, level_id: str, semester: str | None = None
    ) -> Sequence[Course]:
        """
        Returns all courses offered by a department and level optionally
        filtered by semester.
        """
        if not (
            isinstance(department_id, str)  # type: ignore
            or not isinstance(level_id, str)  # type: ignore
        ):
            raise ValueError("department_id and level_id must be a valid str.")

        if semester and semester.lower() not in ["first", "second"]:
            raise ValueError("semester must be either first or second.")

        stmt = (
            select(Course)
            .join(Course.departments)
            .where(
                Course.level_id == level_id,
                Department.id == department_id,  # type: ignore
            )
        )

        if semester:
            stmt = stmt.where(Course.semester == Semester(semester.lower()))

        courses = self.__session.scalars(stmt).all()
        return courses

    def new(self, obj: BaseModel) -> None:
        """Add a new object to the current session."""
        self.__session.add(obj)

    def reload(self) -> None:
        """Create database tables and initialize the session factory."""
        # Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )

    def save(self) -> None:
        """Commit the current transaction, rollback if an error occurs."""
        try:
            self.__session.commit()
        except Exception as e:
            try:
                self.__session.rollback()
            except Exception as rollback_error:
                logger.critical(f"Rollback failed: {rollback_error}")
            raise e

    def search_email(self, email: str) -> Optional[User]:
        """
        Checks for a user email in the database.
        Returns email if found else None.
        """
        if not isinstance(email, str):  # type: ignore
            return

        user = self.__session.scalars(
            select(User).where(User.email == email)
        ).one_or_none()
        return user
