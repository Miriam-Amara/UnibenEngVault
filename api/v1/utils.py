#!/usr/bin/env python3

"""

"""


from datetime import datetime
from flask import request, abort
import logging

from api.v1.data_validations import DatabaseOp
from models import storage
from models.basemodel import BaseModel
from models.user import User, UserWarning, UserSuspension
from models.admin import Admin


logger = logging.getLogger(__name__)


def get_obj(cls: str, id: str) -> BaseModel | None:
    """
    """
    try:
        return storage.get(cls, id)
    except Exception as e:
        logger.error(f"{e}")
        abort(500, description="Database operation failed.")


def get_request_data():
    """
    """
    try:
        request_json_data = request.get_json()
    except Exception:
        abort(400, description="Not a json")
    return request_json_data


class UserDisplineHandler:
    """
    """
    SUSPENSION_INTERVAL = 3
    MAX_WARNINGS = 9
    TERMINATION_LIMIT = 3

    def should_suspend_user(self, user: User) -> bool:
        """
        """
        warnings = user.warnings_count
        
        return (
            warnings % self.SUSPENSION_INTERVAL == 0
            and warnings <= self.MAX_WARNINGS
        )

    def should_terminate_account(self, user: User) -> bool:
        """
        """
        return user.suspensions_count >= self.TERMINATION_LIMIT

    def create_user_warning(
            self, user: User, admin: Admin,
            reason: str, db: DatabaseOp
        ) -> UserWarning:
        """
        """
        warning = UserWarning(reason=reason, user_id=user.id, admin_id=admin.id)
        user.warnings_count += 1
        db.save(warning)
        db.save(user)
        return warning

    def handle_suspension(self, user: User, db: DatabaseOp) -> None:
        """
        """
        if self.should_suspend_user(user):
            suspension = UserSuspension(duration_days=7, user_id=user.id)
            user.suspensions_count += 1
            user.is_active = False
            db.save(suspension)
            db.save(user)
        
    def handle_termination(self, user: User, db: DatabaseOp) -> None:
        """
        """
        if not self.should_terminate_account(user):
            return
        db.delete(user)
        try:
            storage.save()
        except Exception as e:
            logger.error(f"{e}")
            abort(500)
    
    def is_user_active(self, user: User, db: DatabaseOp) -> bool:
        """
        """
        # suspension has not expired
        logger.debug(f"{user.suspension}")
        if user.suspension.expires_at > datetime.now():
            return False
        
        # suspension has expired
        if not user.is_active:
            user.is_active = True
            db.save(user)
        return True
