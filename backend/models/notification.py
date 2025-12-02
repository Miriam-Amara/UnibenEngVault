#!/usr/bin/env python3

"""Defines notification model for the system."""


from datetime import datetime
from sqlalchemy import Table, Column, String, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, relationship

from models.basemodel import BaseModel, Base


notification_reads = Table(
    "notification_reads",
    Base.metadata,
    Column(
        "notification_id",
        String(36),
        ForeignKey("notifications.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "admin_id",
        String(36),
        ForeignKey("admins.id", ondelete="CASCADE"),
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

    message = mapped_column(String(2000), nullable=False)

    admin = relationship(
        "Admin",
        secondary="notification_reads",
        back_populates="notifications",
    )
    
    # @classmethod
    # def get_notifications(cls, user: User):
    #     """
    #     """
    #     from models import storage
    #     return storage.get_user_notifications(user)