#!/usr/bin/env python3

"""Defines the File model for the system."""

from sqlalchemy import String, Integer, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, relationship
import enum

from models.basemodel import BaseModel, Base


class FileStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class Scope(enum.Enum):
    general = "general"
    departmental = "departmental"


class File(BaseModel, Base):
    """
    Represents an academic file or course material in the system.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to File, e.g., file_name, file_type, etc.)
    """

    __tablename__ = "files"

    file_name = mapped_column(String(200), nullable=False)
    file_type = mapped_column(String(100), nullable=False)
    scope = mapped_column(Enum(Scope), nullable=False, default="departmental")
    file_format = mapped_column(String(10), nullable=False)
    session = mapped_column(String(20))
    size = mapped_column(Integer, nullable=False)  # in kilobytes
    status = mapped_column(Enum(FileStatus), nullable=False, default="pending")
    rejection_reason = mapped_column(String(1024))
    filepath = mapped_column(String(300), nullable=False)
    course_id = mapped_column(
        String(36), ForeignKey("courses.id"), nullable=False
    )
    user_id = mapped_column(String(36), ForeignKey("users.id"))
    admin_id = mapped_column(String(36), ForeignKey("admins.id"))

    course = relationship("Course", back_populates="files", viewonly=True)
    added_by = relationship(
        "User", back_populates="course_files_added", viewonly=True
    )
    approved_by = relationship(
        "Admin", back_populates="approved_files", viewonly=True
    )
