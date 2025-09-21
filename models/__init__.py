#!/usr/bin/env python3


from dotenv import load_dotenv
import os

from models.engine.db_storage import DBStorage


load_dotenv()


if os.getenv("UNIBENENGVAULT_ENV") == "test":
    db_url = os.getenv("DATABASE_URL_TEST")
    if not db_url:
        raise ValueError("No test database found")
    
    storage = DBStorage(database_url=db_url)
    storage.reload()
