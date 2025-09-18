#!/usr/bin/env python3

"""Defines user-related models for the system."""


from datetime import datetime
from sqlalchemy import String, ForeignKey, Enum, Boolean, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Sequence, cast
import enum
import logging

from models.basemodel import BaseModel, Base


logger = logging.getLogger(__name__)

class Role(enum.Enum):
    student = "student"
    admin = "admin"


class User(BaseModel, Base):
    """
    Represents a user of the system.

    A user can either be a student or an admin.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to User, e.g., email, password, role, etc.)
    """

    __tablename__ = "users"

    email = mapped_column(String(100), unique=True, nullable=False)
    password = mapped_column(String(200), nullable=False)
    role = mapped_column(Enum(Role), nullable=False, default=Role.student)
    email_verified = mapped_column(Boolean, nullable=False, default=False)
    is_active = mapped_column(Boolean, nullable=False, default=True)
    warnings_count = mapped_column(Integer, nullable=False, default=0)
    suspensions_count = mapped_column(Integer, nullable=False, default=0)
    department_id = mapped_column(
        String(36), ForeignKey("departments.id"), nullable=False
    )
    level_id = mapped_column(
        String(36), ForeignKey("levels.id"), nullable=False
    )

    department = relationship("Department", back_populates="users")
    level = relationship("Level", back_populates="users")
    warnings = relationship(
        "UserWarning", back_populates="issued_to", viewonly=True
    )
    suspension = relationship(
        "UserSuspension", back_populates="issued_to", viewonly=False, uselist=False
    )
    admin = relationship(
        "Admin", back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    course_files_added = relationship(
        "File", back_populates="added_by", viewonly=True
    )
    tutorial_links_added = relationship(
        "TutorialLink", back_populates="added_by", viewonly=True
    )
    feedbacks_added = relationship(
        "Feedback", back_populates="added_by", viewonly=True
    )
    helps_added = relationship(
        "Help", back_populates="added_by", viewonly=True
    )
    reports_added = relationship(
        "Report", back_populates="added_by", viewonly=True
    )

    @classmethod
    def get_users_by_deparment_and_level(
        cls,
        department_id: str, level_id: str,
        page_size: int, page_num: int
    ):
        """
        """
        from models import storage
        user_objects: Sequence[User] | None = cast(Sequence[User], storage.get_by_department_and_level(
            "User",
            department_id, level_id,
            page_size, page_num
        ))
        return user_objects
    
    @classmethod
    def search(cls, email: str):
        """
        """
        from models import storage
        return storage.search_by_email(email)
        


class UserWarning(BaseModel, Base):
    """
    Represents a warning issued to a user.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to UserWarning, e.g., user_id, reason, etc.)
    """

    __tablename__ = "user_warnings"

    reason = mapped_column(String(1024), nullable=False)
    user_id = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    admin_id = mapped_column(
        String(36), ForeignKey("admins.id"), nullable=False
    )

    issued_to: Mapped[User] = relationship(
        "User", back_populates="warnings", viewonly=False, uselist=False
    )
    issued_by = relationship(
        "Admin", back_populates="user_warnings_issued", viewonly=True
    )


class UserSuspension(BaseModel, Base):
    """
    Represents a suspension applied to a user.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to UserSuspension, e.g., user_id, etc.)
    """

    __tablename__ = "user_suspensions"

    duration_days = mapped_column(Integer, nullable=False, default=0)
    expires_at = mapped_column(
        DateTime, nullable=False, default=datetime.now, sort_order=-2
    )
    user_id = mapped_column(
        String(36), ForeignKey("users.id"), unique=True, nullable=False
    )

    issued_to = relationship(
        "User", back_populates="suspension", viewonly=True
    )
