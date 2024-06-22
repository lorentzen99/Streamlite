import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_username = os.getenv('STREAMLITE_DB_USERNAME')
db_password = os.getenv('STREAMLITE_DB_PASSWORD')

# Note the use of "postgresql+asyncpg" for async support
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{db_username}:{db_password}@localhost:5433/streamlite"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()