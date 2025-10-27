#!/usr/bin/env python3

"""
Defines the Department model for the system.
"""

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship

from models.basemodel import BaseModel, Base


class Department(BaseModel, Base):
    """
    Represents a department within a faculty.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to Department, e.g., dept_name, etc.)
    """

    __tablename__ = "departments"

    dept_name = mapped_column(String(200), unique=True, nullable=False)
    dept_code = mapped_column(String(20), unique=True, nullable=False)
    users = relationship(
        "User",
        back_populates="department",
    )

    from models.course import course_departments
    courses = relationship(
        "Course",
        secondary="course_departments",
        back_populates="departments",
    )
    admin_permissions = relationship(
        "AdminPermission",
        back_populates="departments",
        cascade="all, delete-orphan",
    )
