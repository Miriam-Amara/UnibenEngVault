#!/usr/bin/env python3

"""

"""

from enum import Enum
from flask import abort, request
from pydantic import (
    BaseModel,
    ValidationError,
    EmailStr,
    StringConstraints,
    PositiveInt,
    StrictBool,
    model_validator,
    field_validator,
)
from typing import Annotated, Any, Optional, Type
import json
import logging


logger = logging.getLogger(__name__)


class FileStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class ReportType(str, Enum):
    file = "file"
    tutorial_link = "tutorial link"
    content = "content"
    other = "other"

class ReportStatus(str, Enum):
    pending = "pending"
    in_progress = "in progress"
    resolved = "resolved"

class ReportPriority(str, Enum):
    normal = "normal"
    high = "high"

class Semester(str, Enum):
    first_semester = "first"
    second_semester = "second"


class CourseCreate(BaseModel):
    """
    """
    course_code: Annotated[
        str,
        StringConstraints(
        pattern=r'^[a-z]{3}\d{3}$',
        min_length=6,
        max_length=6,
        strip_whitespace=True
    )]
    semester: Semester
    credit_load: Annotated[int, PositiveInt]
    title: Annotated[
        str,
        StringConstraints(min_length=3, max_length=500)
    ]
    level_id: Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            strip_whitespace=True
        )
    ]
    outline: Annotated[
        str,
        StringConstraints(min_length=5, max_length=2000)
    ]
    is_active: Optional[StrictBool] = True

    @field_validator("credit_load")
    @classmethod
    def check_constraints(cls, credit_load: int) -> int:
        """
        """
        if credit_load < 1 or credit_load > 10:
            raise ValueError(
                "Credit load must not be less than one or greater than ten"
            )
        return credit_load

    @model_validator(mode="before")
    @classmethod
    def set_to_lowercase(cls, request_data: Any):
        """
        """
        for attr, value in request_data.items():
            if isinstance(value, str):
                request_data[attr] = value.lower()
        return request_data


class CourseUpdate(BaseModel):
    """
    """
    course_code: Optional[Annotated[
        str,
        StringConstraints(
        pattern=r'^[a-z]{3}\d{3}$',
        min_length=6,
        max_length=6,
        strip_whitespace=True
    )]] = None
    semester: Optional[Semester] = None
    credit_load: Optional[Annotated[int, PositiveInt]] = None
    level_id: Optional[Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            strip_whitespace=True
        )
    ]] = None
    title: Optional[Annotated[
        str,
        StringConstraints(min_length=3, max_length=500)
    ]] = None
    outline: Optional[Annotated[
        str,
        StringConstraints(min_length=5, max_length=2000)
    ]] = None
    is_active: Optional[StrictBool] = None

    @field_validator("credit_load")
    @classmethod
    def check_constraints(cls, credit_load: int) -> int:
        """
        """
        if credit_load < 1 or credit_load > 10:
            raise ValueError(
                "Credit load must not be less than one or greater than ten"
            )
        return credit_load

    @model_validator(mode="before")
    @classmethod
    def set_to_lowercase(cls, request_data: Any):
        """
        """
        for attr, value in request_data.items():
            if isinstance(value, str):
                request_data[attr] = value.lower()
        return request_data


class DepartmentCreate(BaseModel):
    """
    """
    dept_name: Annotated[
        str,
        StringConstraints(
            pattern=r".*\bengineering$",
            strip_whitespace=True
        )
    ]
    dept_code: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=3,
            strip_whitespace=True
        )
    ]

    @model_validator(mode="before")
    @classmethod
    def set_to_lowercase(cls, request_data: Any):
        """
        """
        for attr, value in request_data.items():
            if isinstance(value, str):
                request_data[attr] = value.lower()
        return request_data


class DepartmentUpdate(BaseModel):
    """
    """
    dept_name: Optional[Annotated[
        str,
        StringConstraints(
            pattern=r".*\bengineering$",
            strip_whitespace=True
        )
    ]] = None
    dept_code: Optional[Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=3,
            strip_whitespace=True
        )
    ]] = None
    
    @model_validator(mode="before")
    @classmethod
    def set_to_lowercase(cls, request_data: Any):
        for attr, value in request_data.items():
            if isinstance(value, str):
                request_data[attr] = value.lower()
        return request_data

class FileCreate(BaseModel):
    """
    """
    file_type: Annotated[
        str,
        StringConstraints(strip_whitespace=True)
    ]
    session: Optional[Annotated[
        str,
        StringConstraints(pattern=r"^\d{4}/\d{4}$", strip_whitespace=True)
    ]] = None

    @field_validator("file_type")
    @classmethod
    def validate_file_type(cls, v: str) -> str:
        """
        """
        valid_file_types = [
            "lecture material", "note", "past question",
            "past questions",
        ]
        if v.lower() not in valid_file_types:
            raise ValueError(
            "file type must be any of these: lecture material, note,"
            "past question, past questions"
        )
        return v.lower()

class FileUpdate(BaseModel):
    """
    """
    file_type: Optional[Annotated[
        str,
        StringConstraints(strip_whitespace=True)
    ]] = None
    session: Optional[Annotated[
        str,
        StringConstraints(
            pattern=r"^\d{4}/\d{4}$",
            strip_whitespace=True
        )
    ]] = None

    status: Optional[FileStatus] = None
    rejection_reason: Optional[Annotated[
        str,
        StringConstraints(
            min_length=5,
            max_length=1024,
            to_lower=True,
            strip_whitespace=True
        )
    ]] = None

    @field_validator("file_type")
    @classmethod
    def validate_file_type(cls, v: str) -> str:
        """
        """
        valid_file_types = [
            "lecture material", "note", "past question",
            "past questions",
        ]
        if v.lower() not in valid_file_types:
            raise ValueError(
            "file type must be any of these: lecture material, note,"
            "past question, past questions"
        )
        return v.lower()
    

class LevelCreate(BaseModel):
    """
    """
    name: Annotated[int, PositiveInt]

    @field_validator("name")
    @classmethod
    def validate_level(cls, v: int) -> int:
        valid_levels = [100, 200, 300, 400, 500, 600]
        if v not in valid_levels:
            raise ValueError(
                "Level must be 100, 200, 300, 400, 500 or 600"
            )
        return v


class ReportCreate(BaseModel):
    """
    """
    report_type: ReportType
    message: Annotated[
        str,
        StringConstraints(
            min_length=5,
            max_length=2000,
            strip_whitespace=True
        )
    ]
    file_id: Optional[Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            strip_whitespace=True
        )
    ]] = None
    tutorial_link_id: Optional[Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            strip_whitespace=True
        )
    ]] = None

    @model_validator(mode="before")
    @classmethod
    def set_to_lowercase(cls, request_data: Any):
        for attr, value in request_data.items():
            if isinstance(value, str):
                request_data[attr] = value.lower()
        return request_data

class ReportUpdate(BaseModel):
    """
    """
    priority: Optional[ReportPriority] = None
    status: Optional[ReportStatus] = None
    response: Optional[Annotated[
        str,
        StringConstraints(
            min_length=5,
            max_length=2000,
            strip_whitespace=True
        )
    ]] = None

    @model_validator(mode="before")
    @classmethod
    def set_to_lowercase(cls, request_data: Any):
        for attr, value in request_data.items():
            if isinstance(value, str):
                request_data[attr] = value.lower()
        return request_data
    

class UserLogin(BaseModel):
    """
    Schema for user login validation.
    """

    email: EmailStr
    password: Annotated[
        str,
        StringConstraints(
            min_length=8,
            max_length=200,
            strip_whitespace=True
        )
    ]

    @field_validator("email")
    @classmethod
    def lowercase_email_username(cls, v: EmailStr) -> EmailStr:
        """
        Convert email/username to lowercase.
        """
        return v.lower()

    @field_validator("password")
    @classmethod
    def check_complexity(cls, v: str):
        """
        Ensure password contains uppercase and digit.
        """
        if not any(c.isupper() for c in v):
            raise ValueError("Must contain an uppercase")
        if not any(c.isdigit() for c in v):
            raise ValueError("Must contain a digit")
        return v

class UserCreate(BaseModel):
    """
    """
    email: EmailStr
    password: Annotated[
        str,
        StringConstraints(
            min_length=8,
            max_length=64,
            strip_whitespace=True
        )
    ]
    is_admin: Optional[StrictBool] = None
    department_id: Optional[Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            strip_whitespace=True
        )
    ]] = None
    level_id: Optional[Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            strip_whitespace=True
        )
    ]] = None

    @field_validator("email")
    @classmethod
    def lowercase_email(cls, v: EmailStr) -> EmailStr:
        return v.lower()
    
    @field_validator("password")
    @classmethod
    def check_complexity(cls, v: Any):
        if not any(c.isupper() for c in v):
            raise ValueError("must contain an uppercase")
        if not any(c.isdigit() for c in v):
            raise ValueError("must contain a digit")
        return v


class UserUpdate(BaseModel):
    """
    """
    is_admin: Optional[StrictBool] = None
    department_id: Optional[Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            strip_whitespace=True
        )
    ]] = None
    level_id: Optional[Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            strip_whitespace=True
        )
    ]] = None


class UserWarningCreate(BaseModel):
    """
    """
    reason: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=1024,
            strip_whitespace=True,
            to_lower=True
        )
    ]


class UserWarningUpdate(BaseModel):
    """
    """
    reason: Optional[Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=1024,
            strip_whitespace=True,
            to_lower=True
        )
    ]] = None
    user_id: Optional[Annotated[
        str,
        StringConstraints(
            min_length=36,
            max_length=36,
            strip_whitespace=True
        )
    ]] = None


def get_request_data() -> dict[str, Any]:
    """
    Extract and validate JSON from the request.
    """
    try:
        request_data: dict[str, Any] = request.get_json()
    except json.JSONDecodeError:
        abort(400, description="Not a json")
    return request_data


def get_file_metadata() -> dict[str, Any]:
    """
    """
    try:
        file_metadata: dict[str, Any] = json.loads(request.form["metadata"])
        logger.debug(f"file_metadata: {file_metadata}")
    except KeyError:
        abort(400, description="Missing key - metadata")
    except json.JSONDecodeError:
        abort(400, description="Not a valid JSON")
    
    logger.debug(f"returned file_metadata: {file_metadata}")
    return file_metadata


def validate_request_data(
        validation_cls: Type[BaseModel]
    ) -> dict[str, Any]:
    """
    """
    if not issubclass(validation_cls, BaseModel):  # type: ignore
        logger.error(
            "Validation class must inherit from pydantic BaseModel"
        )
        abort(500)

    if validation_cls is FileCreate:
        request_data = get_file_metadata()
    else:
        request_data = get_request_data()

    try:
        valid_data: BaseModel = validation_cls(**request_data)
    except ValidationError as e:
        abort(400, description=e.errors())

    if not valid_data.model_dump(exclude_none=True):
        abort(400, description="Request data cannot be empty.")
    return valid_data.model_dump(exclude_unset=True)
