#!/usr/bin/env python3

"""Defines the Course model for the system."""

from sqlalchemy import String, Integer, Boolean, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, relationship
import enum

from models.basemodel import BaseModel, Base


class Semester(enum.Enum):
    first = "first"
    second = "second"


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

    course_code = mapped_column(String(36), nullable=False, unique=True)
    semester = mapped_column(Enum(Semester), nullable=False)
    credit_load = mapped_column(Integer, nullable=False)
    is_optional = mapped_column(Boolean, nullable=False, default=False)
    title = mapped_column(String(500), nullable=False)
    outline = mapped_column(String(2000), nullable=False)
    is_active = mapped_column(Boolean, nullable=False, default=True)
    department_id = mapped_column(ForeignKey("departments.id"), nullable=False)
    level_id = mapped_column(ForeignKey("levels.id"), nullable=False)
    admin_id = mapped_column(ForeignKey("admins.id"))

    department = relationship(
        "Department", back_populates="courses", viewonly=True
    )
    level = relationship("Level", back_populates="courses", viewonly=True)
    registered_by = relationship(
        "Admin", back_populates="courses_registered", viewonly=True
    )
    files = relationship(
        "File", back_populates="course",
        viewonly=True, cascade="all, delete-orphan"
    )
