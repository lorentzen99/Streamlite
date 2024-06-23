from dotenv import load_dotenv
load_dotenv()

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_host = os.getenv('POSTGRES_HOST')
db_port = os.getenv('POSTGRES_PORT')
db_username = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_name = os.getenv('POSTGRES_DB')

# Note the use of "postgresql+asyncpg" for async support
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()
