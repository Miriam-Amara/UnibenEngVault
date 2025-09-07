#!/usr/bin/env python3

"""

"""

from enum import Enum
from flask import abort, jsonify
from pydantic import BaseModel, ValidationError, EmailStr
from pydantic import model_validator, field_validator, constr, conint
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from typing import Any, Optional
import logging

from api.v1.utils import get_request_data


logger = logging.getLogger(__name__)


class Role(str, Enum):
    student = "student"
    admin = "admin"

class CourseCreate(BaseModel):
    """
    """
    course_code: constr(pattern=r'^[a-z]{3}\d{3}$', min_length=6, max_length=6, strip_whitespace=True) # type: ignore
    semester: str
    credit_load: conint(ge=1, le=6) # type: ignore
    title: constr(min_length=3, max_length=500) # type: ignore
    outline: constr(min_length=10, max_length=2000) # type: ignore
    is_active: bool = True
    department_id: str
    level_id: str

    @model_validator(mode="before")
    def set_to_lowercase(cls, v: Any):
        return v.lower() if isinstance(v, str) else v


class CourseUpdate(BaseModel):
    course_code: Optional[constr(pattern=r'^[a-z]{3}\d{3}$', min_length=6, max_length=6, strip_whitespace=True)] = None # type: ignore
    semester: Optional[str] = None
    credit_load: Optional[conint(ge=1, le=6)] = None # type: ignore
    title: Optional[constr(min_length=3, max_length=500)] = None # type: ignore
    outline: Optional[constr(min_length=10, max_length=2000)] = None # type: ignore
    is_active: Optional[bool] = True
    department_id: Optional[str] = None
    level_id: Optional[str] = None

    @model_validator(mode="before")
    def set_to_lowercase(cls, v: Any):
        return v.lower() if isinstance(v, str) else v


class DepartmentCreate(BaseModel):
    """
    """
    dept_name: constr(pattern=r".*\bengineering$", strip_whitespace=True) # type: ignore
    dept_code: constr(min_length=3, max_length=3, strip_whitespace=True) # type: ignore

    @model_validator(mode="before")
    def set_to_lowercase(cls, v: Any):
        return v.lower() if isinstance(v, str) else v


class DepartmentUpdate(BaseModel):
    """
    """
    dept_name: Optional[constr(pattern=r".*\bengineering$", strip_whitespace=True)] = None # type: ignore
    dept_code: Optional[constr(min_length=3, max_length=3, strip_whitespace=True)] = None # type: ignore

    @model_validator(mode="before")
    def set_to_lowercase(cls, v: Any):
        return v.lower() if isinstance(v, str) else v


class LevelCreate(BaseModel):
    """
    """
    name: conint(ge=100, le=500) # type: ignore


class LevelUpdate(BaseModel):
    name: Optional[conint(ge=100, le=500)] = 0 # type: ignore


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=64, strip_whitespace=True) # type: ignore
    role: Role = Role.student
    department_id: constr(min_length=36, max_length=36, strip_whitespace=True) # type: ignore
    level_id: constr(min_length=36, max_length=36, strip_whitespace=True) # type: ignore

    @field_validator("password")
    def check_complexity(cls, v: Any):
        if not any(c.isupper() for c in v):
            raise ValueError("must contain an uppercase")
        if not any(c.isdigit() for c in v):
            raise ValueError("must contain a digit")
        return v

    @model_validator(mode="before")
    def set_to_lowercase(cls, v: Any):
        return v.lower() if isinstance(v, str) else v


class UserUpdate(BaseModel):
    role: Optional[Role] = None
    department_id: Optional[str] = None
    level_id: Optional[str] = None


class ValidateData:
    """
    """
    validation_classes: dict[str, Any] = {
        "DepartmentCreate": DepartmentCreate,
        "DepartmentUpdate": DepartmentUpdate,
        "LevelCreate": LevelCreate,
        "LevelUpdate": LevelUpdate,
        "CourseCreate": CourseCreate,
        "CourseUpdate": CourseUpdate,
        "UserCreate": UserCreate,
        "UserUpdate": UserUpdate,
    }

    def validate_request_data(self, validation_cls: str) -> dict[str, Any] | None:
        """
        """
        if validation_cls not in self.validation_classes:
            return
        request_data = get_request_data()

        try:
            valid_data: BaseModel = self.validation_classes[validation_cls](**request_data)
        except ValidationError as e:
            logger.error(f"{e}")
            friendly_errors: list[dict[str, Any]] = [
                {"field": ".".join(str(loc) for loc in err["loc"]), "message": err["msg"]}
                for err in e.errors()
            ]
            abort(jsonify({"errors": friendly_errors}), 400)
        
        if validation_cls == "UserCreate" or validation_cls == "UserUpdate":
            return valid_data.model_dump(exclude_none=True) 
        return valid_data.model_dump(exclude_unset=True)
    

class DatabaseOp:
    """
    """
    from models.basemodel import BaseModel
    def save(self, obj: BaseModel):
        """
        """
        try:
            obj.save()
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                detail = e.orig.diag.message_detail
                abort(400, description=detail)
            else:
                logger.error(f"{e}")
                abort(400, description="Database operation failed.")
        except Exception as e:
            logger.error(f"{e}")
            abort(400, description="Database operation failed.")

    def delete(self, obj: BaseModel):
        """
        """
        try:
            obj.delete()
        except Exception as e:
            logger.error(f"{e}")
            abort(400, description="Database operation failed.")
