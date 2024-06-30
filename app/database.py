import asyncio
from dotenv import load_dotenv
load_dotenv()
import os
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory
from sqlalchemy.ext.asyncio import AsyncEngine

DB_HOST = os.getenv('POSTGRES_HOST', "db")
DB_PORT = os.getenv('POSTGRES_PORT', "5432")
DB_USERNAME = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_NAME = os.getenv('POSTGRES_DB', "streamlite")

# Note the use of "postgresql+asyncpg" for async support
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()

async def init_db(engine):
    async with engine.begin() as connection:  # Use engine's connection directly
        await connection.run_sync(Base.metadata.create_all)

ALEMBIC_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "alembic.ini")
async def run_migrations(engine):
    config = Config(ALEMBIC_CONFIG_PATH)
    # This line is problematic as it sets the engine directly; instead, we should use a connection
    # config.attributes['connection'] = engine
    async with engine.connect() as connection:
        config.attributes['connection'] = connection  # Set the connection instead of engine
        script = ScriptDirectory.from_config(config)
        async with connection.begin():
            context = EnvironmentContext(
                config,
                script,
                fn=lambda rev, context: script._upgrade_revs("head", rev),
                asynchronous=True
            )
            await context.run_migrations()

async def setup_database(engine):
    await init_db(engine)
    await run_migrations(engine)

asyncio.run(setup_database(engine))


"""async def test_db_connection():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT version();"))
        version = result.fetchone()
        print(f"Connected to PostgreSQL version: {version[0]}")
asyncio.run(test_db_connection()) # Uncomment to test connection"""
