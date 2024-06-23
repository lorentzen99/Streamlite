import asyncio
from dotenv import load_dotenv
load_dotenv()

import os
from sqlalchemy import text
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
print(f"Connecting to database with URL: {SQLALCHEMY_DATABASE_URL}")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()

async def run_migrations():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def test_db_connection():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT version();"))
        version = result.fetchone()
        print(f"Connected to PostgreSQL version: {version[0]}")

# asyncio.run(test_db_connection()) # Uncomment to test connection
