#!/usr/bin/env python3

"""
Initializes database storage based on the current environment.
"""

from dotenv import load_dotenv
from typing import cast
import os

from models.engine.db_storage import DBStorage


load_dotenv()


prod_db_url = os.getenv("PRODUCTION_DB_URL")
dev_db_url = os.getenv("DEVELOPMENT_DB_URL")
test_db_url = os.getenv("TEST_DB_URL")
env = os.getenv("FLASK_ENV", "production")

if env == "production" and not prod_db_url:
    raise ValueError("No PRODUCTION_DB_URL env variable found.")

if env == "development" and not dev_db_url:
    raise ValueError("No DEVELOPMENT_DB_URL env variable found.")

if env == "test" and not test_db_url:
    raise ValueError("No TEST_DB_URL env variable found.")


if env == "development":
    database_url = dev_db_url
elif env == "test":
    database_url = test_db_url
else:
    database_url = prod_db_url

storage = DBStorage(cast(str, database_url))
storage.reload()
