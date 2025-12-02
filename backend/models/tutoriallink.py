#!/usr/bin/env python3

"""Defines tutorial_link model for the system."""


from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, relationship
import enum

from models.basemodel import BaseModel, Base


class TutorialLinkStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ContentType(str, enum.Enum):
    video = "video"
    blog = "blog"
    article = "article"
    pdf = "pdf"
    audio = "audio"
    other = "other"


class TutorialLink(BaseModel, Base):
    """
    Represents an external tutorial resource linked to a course.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to TutorialLink, e.g., url, course_id, etc.)
    """

    __tablename__ = "tutorial_links"

    course_id = mapped_column(
        String(36), ForeignKey("courses.id"), nullable=False
    )
    url = mapped_column(String(1024), nullable=False)
    title = mapped_column(String(200), nullable=False)
    content_type = mapped_column(
        Enum(
            ContentType,
            name="content_type",
            create_type=True
        ),
        nullable=False
    )
    status = mapped_column(
        Enum(
            TutorialLinkStatus,
            name="tutorial_link_status",
            create_type=True
        ),
        nullable=False, default="pending"
    )
    level_id = mapped_column(
        ForeignKey("levels.id", ondelete="SET NULL")
    )
    user_id = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL")
    )
    admin_id = mapped_column(
        String(36), ForeignKey("admins.id", ondelete="SET NULL")
    )

    added_by = relationship(
        "User", back_populates="tutorial_links_added"
    )
    approved_by = relationship(
        "Admin", back_populates="tutorial_links_approved"
    )
    level = relationship(
        "Level", back_populates="tutorial_links"
    )
