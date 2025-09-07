#!/usr/bin/env python3
"""

"""

from logging_config import setup_logging

setup_logging()

from models.basemodel import BaseModel, Base # type: ignore
from models.admin import Admin, Permission, AdminPermission # type: ignore
from models.course import Course # type: ignore
from models.department import Department # type: ignore
from models.feedback import Feedback # type: ignore
from models.file import File # type: ignore
from models.help import Help # type: ignore
from models.level import Level # type: ignore
from models.notification import Notification # type: ignore
from models.report import Report # type: ignore
from models.tutoriallink import TutorialLink # type: ignore
from models.user import User # type: ignore
from models.department_level_courses import DepartmentLevelCourses # type: ignore
