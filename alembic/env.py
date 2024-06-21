from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.database import Base  # Adjust this import based on your application's structure
from app.api.models.user import User  # Adjust imports for all relevant models

# Alembic configuration object
config = context.config

# Configure Python logging based on the Alembic config file
if config.config_file_name:
    fileConfig(config.config_file_name)

# Define the metadata to target for migrations
target_metadata = Base.metadata

# Define migration modes

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# Determine the migration mode and execute accordingly
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
