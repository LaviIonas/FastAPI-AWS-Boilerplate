import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from main import app
from database import get_db, Base
from config import settings
from oauth2 import create_access_token
from models import *

# Test database URL
SQLALCHEMY_TEST_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

# Create test database engine
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)

# Create TestingSessionLocal class
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
