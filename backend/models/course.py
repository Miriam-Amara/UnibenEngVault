#!/usr/bin/env python3

"""Defines the Course model for the system."""

from sqlalchemy import String, Integer, Boolean, ForeignKey, Enum
from sqlalchemy import Table, Column
from sqlalchemy.orm import mapped_column, relationship
import enum

from models.basemodel import BaseModel, Base


class Semester(enum.Enum):
    first = "first"
    second = "second"


course_departments = Table(
    "course_departments",
    Base.metadata,
    Column(
        "course_id",
        String(36),
        ForeignKey("courses.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "department_id",
        String(36),
        ForeignKey("departments.id", ondelete="CASCADE"),
        primary_key=True,
    )
)

class Course(BaseModel, Base):
    """
    Represents a course offered in the system.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to Course, e.g., course_code, etc.)
    """

    __tablename__ = "courses"

    course_code = mapped_column(String(6), nullable=False, unique=True)
    semester = mapped_column(Enum(Semester), nullable=False)
    credit_load = mapped_column(Integer, nullable=False)
    title = mapped_column(String(500), nullable=False)
    outline = mapped_column(String(2000), nullable=False)
    is_active = mapped_column(Boolean, nullable=False, default=True)
    level_id = mapped_column(ForeignKey("levels.id"), nullable=False)
    admin_id = mapped_column(ForeignKey("admins.id", ondelete="SET NULL"))

    level = relationship(
        "Level",
        back_populates="courses"
    )
    added_by = relationship(
        "Admin",
        back_populates="courses_added"
    )
    files = relationship(
        "File",
        back_populates="course",
        cascade="all, delete-orphan"
    )
    departments = relationship(
        "Department",
        secondary="course_departments",
        back_populates="courses"
    )

    @classmethod
    def search_course_code(cls, course_code: str):
        """
        """
        from models import storage
        return storage.search_course_code(course_code)
