#!/usr/bin/env python3

"""

"""

from typing import Any

user_data: list[dict[str, Any]] = [
    {"email": "firstuser@gmail.com", "password": "Firstuser1234", "is_admin": True},
    {"email": "seconduser@gmail.com", "password": "Seconduser1234"},
    {"email": "thirduser@gmail.com", "password": "Thirduser1234"},
    {"email": "fourthuser@gmail.com", "password": "Fourthuser1234"},
    {"email": "fifthuser@gmail.com", "password": "Fifthuser1234"},
]

department_data: list[dict[str, str]] = [
    {"dept_name": "agricultural engineering", "dept_code": "age"},
    {"dept_name": "COMPUTER ENGINEERING", "dept_code": "cpe"},
    {"dept_name": "Chemical Engineering", "dept_code": "che"},
    {"dept_name": "civil engineering", "dept_code": "cve"},
    {"dept_name": "electrical engineering", "dept_code": "eee"},
    {"dept_name": "mechanical engineering", "dept_code": "mee"},
    {"dept_name": "mechatronics engineering", "dept_code": "mte"},
    {"dept_name": "marine engineering", "dept_code": "mre"},
    {"dept_name": "material and metallurgical engineering", "dept_code": "mme"},
    {"dept_name": "industrial engineering", "dept_code": "ide"},
    {"dept_name": "petroleum engineering", "dept_code": "pee"},
    {"dept_name": "production engineering", "dept_code": "pre"},
    {"dept_name": "structural engineering", "dept_code": "ste"}
]

level_data = [
    {"name": 100},
    {"name": 200},
    {"name": 300},
    {"name": 400},
    {"name": 500},
]

course_data: list[dict[str, Any]] = [
    {
        "course_code": "IDE231",
        "semester": "FIRST",
        "credit_load": 2,
        "title": "Engineering Statistics",
        "outline": "Engineering Statistics",
    },
    {
        "course_code": "CVE212",
        "semester": "FIRST",
        "credit_load": 3,
        "title": "Civil Engineering Sheer Stress",
        "outline": "Sheer Stress and bearing",
    },
    {
        "course_code": "MEE212",
        "semester": "FIRST",
        "credit_load": 2,
        "title": "MECHANICAL ENGINEERING COURSE",
        "outline": "MECHANICAL ENGINEERING COURSE",
    },
    {
        "course_code": "EMA282",
        "semester": "FIRST",
        "credit_load": 4,
        "title": "Engineering mathematics",
        "outline": "Engineering mathematics",
    },
    {
        "course_code": "PRE245",
        "semester": "FIRST",
        "credit_load": 3,
        "title": "Machine tools and practice",
        "outline": "Machine tools and Practice",
    },
]

