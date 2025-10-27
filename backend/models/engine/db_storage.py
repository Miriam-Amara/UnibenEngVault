#!usr/bin/env python3

"""
Database storage engine for managing ORM operations with SQLAlchemy.
"""

from dotenv import load_dotenv
from typing import Any, Optional, Sequence, Type, TypeVar
from sqlalchemy import  create_engine, select, and_, or_, func
from sqlalchemy.orm import sessionmaker, scoped_session
import logging

from models.basemodel import BaseModel, Base
from models.admin import Admin, Permission, AdminPermission
from models.course import Course, course_departments
from models.department import Department
from models.feedback import Feedback
from models.file import File
from models.help import Help
from models.level import Level
from models.notification import Notification, notification_reads, NotificationScope
from models.report import Report
from models.tutoriallink import TutorialLink
from models.user import User
from models.user_session import UserSession


load_dotenv()
logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


class DBStorage:
    """Manages database interactions using SQLAlchemy ORM."""

    __classes: list[Type[BaseModel]] = [
        Admin,
        Permission, 
        AdminPermission,
        Course,
        Department,
        Feedback,
        File,
        Help,
        Level,
        Notification,
        Report,
        TutorialLink,
        User,
        UserSession,
    ]

    def __init__(self, database_url: str) -> None:
        """Initialize the database engine."""
        self.__engine = create_engine(database_url, pool_pre_ping=True)
        
    def all(
        self, cls: Type[T], page_size: int, page_num: int
    ) -> Sequence[T]:
        """Return all objects or objects of a given class with pagination."""
        if page_size <= 0:
            raise ValueError(f"{page_size} must be greater than zero")
        if page_num <= 0:
            raise ValueError(f"{page_num} must be greater than zero")
        if not isinstance(page_size, int):   # type: ignore
            raise TypeError(f"{page_size} should be a valid integer.")
        if not isinstance(page_num, int):   # type: ignore
            raise TypeError(f"{page_num} should be a valid integer.")
        if not issubclass(cls, BaseModel):  # type: ignore
            raise TypeError("cls must inherit from BaseModel")
        
        cls_objects = self.__session.scalars(
            select(cls)
            .offset((page_num - 1) * page_size)
            .limit(page_size)
        ).all()
        return cls_objects

    def close(self) -> None:
        """Close the current database session."""
        self.__session.close()

    def count(self, cls: Type[T] | None = None) -> int | dict[str, Any] | None:
        """
        Return the total number of objects of a class
        or all classes in storage.
        """
        if cls in self.__classes:
            cls_objects_count = self.__session.scalar(
                select(func.count()).select_from(cls)
            )
            return cls_objects_count

        all_obj_count: dict[str, Any] = {}
        for cls_name in self.__classes:
            cls_objects_count = self.__session.scalar(
                select(func.count()).select_from(cls_name)
            )
            all_obj_count[cls_name.__name__] = cls_objects_count
        return all_obj_count
    
    # def count_course_departments(
    #         self, course_id: str,
    #     ) -> Optional[int]:
    #     """
    #     """
    #     assert self.__session is not None, "Session has not been initialized"

    #     course_department_count = self.__session.scalar(
    #             select(func.count())
    #             .select_from(course_departments)
    #             .where(course_departments.c.course_id == course_id)
    #         )
    #     return course_department_count

    
    # def count_courses_by_department_and_level(
    #         self, level_id: str, semester: str
    #     ) -> Optional[Sequence[Any]]:
    #     """
    #     """
    #     assert self.__session is not None, "Session has not been initialized"

    #     total_departments = self.count("Department")
    #     if not total_departments:
    #         return
        
    #     course_dept_counts = (
    #         select(
    #             course_departments.c.course_id,
    #             func.count(course_departments.c.department_id).label("dept_count")
    #         )
    #         .group_by(course_departments.c.course_id)
    #         .subquery()
    #     )

    #     stmt = (
    #         select(
    #             func.count().filter(
    #                 course_dept_counts.c.dept_count == 1
    #             ).label("department_specific"),
    #             func.count().filter(
    #                 (course_dept_counts.c.dept_count > 1) &
    #                 (course_dept_counts.c.dept_count < total_departments)
    #             ).label("shared"),
    #             func.count().filter(
    #                 course_dept_counts.c.dept_count == total_departments
    #             ).label("general"),
    #         )
    #         .select_from(Course)
    #         .join(course_dept_counts, Course.id == course_dept_counts.c.course_id) # type: ignore
    #         .where(
    #             Course.level_id == level_id,
    #             Course.semester == semester
    #         )
    #     )
    #     courses_count = self.__session.scalars(stmt).all()
    #     return courses_count


    def delete(self, obj: BaseModel) -> None:
        """Delete an object from the current session."""
        self.__session.delete(obj)

    def get_obj_by_id(self, cls: Type[T], id: str) -> T | None:
        """
        Returns the object based on the class and its ID, or None if not found.
        """
        if issubclass(cls, BaseModel):  # type: ignore
            obj = self.__session.get(cls, id)
            return obj
    
    def get_users_by_dept_and_level(
            self,
            department_id: str, level_id: str,
            page_size:int, page_num:int,
        ) -> Sequence[User] | None:
        """
        """
        if (not isinstance(department_id, str)  # type: ignore
            or not isinstance(level_id, str)  # type: ignore
        ):
            return
        
        user_objects = self.__session.scalars(
            select(User).where(
                and_(User.department_id == department_id,
                     User.level_id == level_id
                    )
                )
            .offset((page_num - 1) * page_size)
            .limit(page_size)
        ).all()
        return user_objects
    
    # def get_courses_by_department_and_level(
    #         self, 
    #         department_id: str, level_id: str,
    #         semester: Optional[str]=None
    #     ) -> Optional[Sequence[BaseModel]]:
    #     """
    #     """
    #     if semester and not isinstance(semester, str): # type: ignore
    #        return
        
    #     if not isinstance(department_id, str) or not isinstance(level_id, str): # type: ignore
    #         return
        
    #     stmt = (
    #         select(Course)
    #         .join(course_departments, Course.id == course_departments.c.course_id) # type: ignore
    #         .where(
    #             Course.level_id == level_id,
    #             course_departments.c.department_id == department_id
    #         )
    #     )
    #     if semester:
    #         stmt = stmt.where(Course.semester == semester)
        
    #     courses = self.__session.scalars(stmt).all()
    #     return courses
    
    def get_user_notifications(self, user: User) -> Sequence[Any]:
        """
        """
        stmt = (
            select(Notification, notification_reads.c.read_at)
            .join(
                notification_reads,
                and_(
                    Notification.__table__.c.id == notification_reads.c.notification_id,
                    notification_reads.c.user_id == user.id
                ),
                isouter=True  # LEFT JOIN so unread notifications are included
            )
            .where(
                and_(
                    or_(
                        Notification.notification_scope == NotificationScope.general,
                        and_(
                            Notification.notification_scope == NotificationScope.group,
                            Notification.department_id == user.department_id,
                            Notification.level_id == user.level_id,
                        ),
                        and_(
                            Notification.notification_scope == NotificationScope.personal,
                            Notification.user_id == user.id,
                        ),
                        and_(
                            Notification.notification_scope == NotificationScope.admin,
                            user.is_admin
                        ),
                    ),
                    notification_reads.c.read_at.is_(None)
                )
            )
            .order_by(Notification.__table__.c.created_at.desc())
        )
        result = self.__session.execute(stmt).all()
        return result

    def new(self, obj: BaseModel) -> None:
        """Add a new object to the current session."""
        self.__session.add(obj)
    
    def reload(self) -> None:
        """Create database tables and initialize the session factory."""
        # Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )

    def save(self) -> None:
        """Commit the current transaction, rollback if an error occurs."""
        try:
            self.__session.commit()
        except Exception as e:
            try:
                self.__session.rollback()
            except Exception as rollback_error:
                logger.critical(f"Rollback failed: {rollback_error}")
            raise e
    
    def search_email(self, email: str) -> Optional[User]:
        """
        """
        if not isinstance(email, str): # type: ignore
            return
        
        user = self.__session.scalars(
            select(User).where(User.email == email)
        ).one_or_none()
        return user
    
    def search_course_code(self, course_code: str) -> Optional[Course]:
        """
        """
        if not isinstance(course_code, str) or len(course_code) != 6: # type: ignore
            return
        
        course = self.__session.scalars(
            select(Course).where(Course.course_code == course_code)
        ).one_or_none()
        return course
