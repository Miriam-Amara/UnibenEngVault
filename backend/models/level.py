#!/usr/bin/env python3

"""Defines level model for the system."""

from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column, relationship

from models.basemodel import BaseModel, Base


class Level(BaseModel, Base):
    """
    Represents an academic level in the system.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to Level, e.g., name, users, courses etc.)
    """

    __tablename__ = "levels"

    level_name = mapped_column(Integer, unique=True, nullable=False)

    admin_permissions = relationship(
        "AdminPermission",
        back_populates="levels",
        cascade="all, delete-orphan"
    )
    courses = relationship("Course", back_populates="level")
    tutorial_links = relationship("TutorialLink", back_populates="level")
    users = relationship("User", back_populates="level")
