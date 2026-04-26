import sys
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy import pool
from dotenv import load_dotenv

# -----------------------------
# PATH
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

# -----------------------------
# ENV
# -----------------------------
load_dotenv(os.path.join(BASE_DIR, ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL is not set")

print("Alembic DB URL =", DATABASE_URL)

# -----------------------------
# MODELS
# -----------------------------
from app.db import Base
from app import models

target_metadata = Base.metadata

# -----------------------------
# ALEMBIC CONFIG
# -----------------------------
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# -----------------------------
# ONLINE
# -----------------------------
def run_migrations_online():

    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,

            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# -----------------------------
# OFFLINE
# -----------------------------
def run_migrations_offline():

    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()