#!/usr/bin/env python3

"""Defines the Report model for the system."""

from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
import enum

from models.basemodel import BaseModel, Base


class ReportType(str, enum.Enum):
    file = "file"
    tutorial_link = "tutorial link"
    content = "content"
    other = "other"


class ReportStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in progress"
    resolved = "resolved"


class ReportPriority(str, enum.Enum):
    normal = "normal"
    high = "high"


class Report(BaseModel, Base):
    """
    Represents a report submitted by a user on platform content or activity.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to Report, e.g., report_type, message, etc.)
    """

    __tablename__ = "reports"

    report_type = mapped_column(
        Enum(ReportType, name="report_type", create_type=True), nullable=False
    )
    message = mapped_column(String(2000), nullable=False)
    priority = mapped_column(
        Enum(ReportPriority, name="report_priority", create_type=True),
        nullable=False, default="normal"
    )
    status = mapped_column(
        Enum(ReportStatus, name="report_status", create_type=True),
        nullable=False, default="pending"
    )
    response = mapped_column(String(2000))
    file_id = mapped_column(
        String(36), ForeignKey("files.id", ondelete="SET NULL")
    )
    tutorial_link_id = mapped_column(
        String(36), ForeignKey("tutorial_links.id", ondelete="SET NULL")
    )
    user_id = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL")
    )
    admin_id = mapped_column(
        String(36), ForeignKey("admins.id", ondelete="SET NULL")
    )

    added_by = relationship(
        "User",
        back_populates="reports_added"
    )
    reviewed_by = relationship(
        "Admin",
        back_populates="reports_reviewed"
    )
