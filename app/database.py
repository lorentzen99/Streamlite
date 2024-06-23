from dotenv import load_dotenv
load_dotenv()

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_HOST = os.getenv('POSTGRES_HOST', "db")
DB_PORT = os.getenv('POSTGRES_PORT', "5432")
DB_USERNAME = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_NAME = os.getenv('POSTGRES_DB', "streamlite")

# FOR LOCAL DB INITIALIZATION TODO REMOVE AT SOME POINT
"""DB_HOST = "localhost"
DB_PORT = "5433"
DB_USERNAME = "user"
DB_PASSWORD = "pw"
DB_NAME = "streamlite"""

# Note the use of "postgresql+asyncpg" for async support
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()
