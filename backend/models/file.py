#!/usr/bin/env python3

"""Defines file model for the system."""

from sqlalchemy import String, Integer, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, relationship
import enum

from models.basemodel import BaseModel, Base


class FileStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


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
    file_ext = mapped_column(String(10), nullable=False)
    file_size = mapped_column(Integer, nullable=False)  # in kilobytes
    session = mapped_column(String(20))
    status = mapped_column(
        Enum(FileStatus, name="file_status", create_type=True),
        nullable=False, default="pending"
    )
    rejection_reason = mapped_column(String(1024))
    temp_filepath = mapped_column(String(300), nullable=False)
    permanent_filepath = mapped_column(String(300))
    course_id = mapped_column(
        String(36), ForeignKey("courses.id", ondelete="SET NULL")
    )
    user_id = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL")
    )
    admin_id = mapped_column(
        String(36), ForeignKey("admins.id", ondelete="SET NULL")
    )

    course = relationship(
        "Course",
        back_populates="files",
    )
    added_by = relationship(
        "User",
        back_populates="course_files_added",
    )
    approved_by = relationship(
        "Admin",
        back_populates="files_approved",
    )
