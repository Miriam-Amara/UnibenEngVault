#!/usr/bin/env python3

"""
Defines user-related models for the system.
"""


from datetime import datetime
from sqlalchemy import (
    String, ForeignKey, Boolean, Integer, DateTime
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Sequence
import logging

from models.basemodel import BaseModel, Base


logger = logging.getLogger(__name__)


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
    is_admin = mapped_column(Boolean, nullable=False, default=False)
    email_verified = mapped_column(Boolean, nullable=False, default=False)
    is_active = mapped_column(Boolean, nullable=False, default=True)
    warnings_count = mapped_column(Integer, nullable=False, default=0)
    suspensions_count = mapped_column(Integer, nullable=False, default=0)
    department_id = mapped_column(
        String(36), ForeignKey("departments.id", ondelete="SET NULL")
    )
    level_id = mapped_column(
        String(36), ForeignKey("levels.id", ondelete="SET NULL")
    )

    department = relationship("Department", back_populates="users")
    level = relationship("Level", back_populates="users")
    warnings = relationship(
        "UserWarning",
        back_populates="issued_to",
    )
    suspension = relationship(
        "UserSuspension",
        back_populates="issued_to",
        cascade="all, delete-orphan",
        uselist=False
    )
    admin = relationship(
        "Admin",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False
    )
    course_files_added = relationship(
        "File", back_populates="added_by"
    )
    tutorial_links_added = relationship(
        "TutorialLink", back_populates="added_by"
    )
    feedbacks_added = relationship(
        "Feedback", back_populates="added_by"
    )
    helps_added = relationship(
        "Help", back_populates="added_by"
    )
    reports_added = relationship(
        "Report", back_populates="added_by"
    )
    user_session = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    @classmethod
    def get_users_by_deparment_and_level(
        cls,
        department_id: str, level_id: str,
        page_size: int, page_num: int
    ):
        """
        Returns users that belond to a specific department and level if found,
        otherwise return None.
        """
        from models import storage
        users: Sequence[User] | None = storage.get_users_by_dept_and_level(
            department_id, level_id, page_size, page_num
        )
        return users
    
    @classmethod
    def search_email(cls, email: str):
        """
        Search for a user email in the database.
        Returns the user if found or None otherwise.
        """
        from models import storage
        return storage.search_email(email)
        


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
    user_id = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"))
    admin_id = mapped_column(String(36), ForeignKey("admins.id", ondelete="SET NULL"))

    issued_to: Mapped[User] = relationship(
        "User", back_populates="warnings", uselist=False
    )
    issued_by = relationship(
        "Admin", back_populates="user_warnings_issued"
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
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False,
    )

    issued_to = relationship("User", back_populates="suspension")
