#!/usr/bin/env python3

"""Defines the Notification model for the system."""


from datetime import datetime
from sqlalchemy import Table, Column, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, relationship
import enum

from models.basemodel import BaseModel, Base
# from models.user import User

class NotificationScope(str, enum.Enum):
    personal = "personal"
    group = "group"
    general = "general"
    admin = "admin"


notification_reads = Table(
    "notifications_reads",
    Base.metadata,
    Column(
        "notification_id",
        String(36),
        ForeignKey("notifications.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "user_id",
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "read_at",
        DateTime,
        default=datetime.now,
        nullable=False,
    )
)

class Notification(BaseModel, Base):
    """
    Represents a notification sent to a user.

    Inherits from:
        BaseModel: Provides id, created_at, updated_at, and common methods.
        Base: SQLAlchemy declarative base for ORM mapping.

    Attributes:
        (class attributes specific to Notification, e.g., message, type, etc.)
    """

    __tablename__ = "notifications"

    notification_scope = mapped_column(
        Enum(NotificationScope, name="notification_scope", create_type=True),
        nullable=False
    )
    message = mapped_column(String(2000), nullable=False)
    department_id = mapped_column(
        String(36), ForeignKey("departments.id", ondelete="SET NULL")
    )
    level_id = mapped_column(
        String(36), ForeignKey("levels.id", ondelete="SET NULL")
    )
    user_id = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL")
    )
    admin_id = mapped_column(
        String(36), ForeignKey("admins.id", ondelete="SET NULL")
    )
    file_id = mapped_column(
        String(36), ForeignKey("files.id", ondelete="SET NULL")
    )
    report_id = mapped_column(
        String(36), ForeignKey("reports.id", ondelete="SET NULL")
    )
    help_id = mapped_column(
        String(36), ForeignKey("helps.id", ondelete="SET NULL")
    )
    feedback_id = mapped_column(
        String(36), ForeignKey("feedbacks.id", ondelete="SET NULL")
    )

    file = relationship("File", backref="notifications", lazy="noload")
    report = relationship("Report", backref="notifications", lazy="noload")
    help = relationship("Help", backref="notifications", lazy="noload")
    feedback = relationship("Feedback", backref="notifications", lazy="noload")
    
    # @classmethod
    # def get_notifications(cls, user: User):
    #     """
    #     """
    #     from models import storage
    #     return storage.get_user_notifications(user)