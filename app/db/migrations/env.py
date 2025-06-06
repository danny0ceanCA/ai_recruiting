# ── BEGIN PATCH ────────────────────────────────────────────────
from logging.config import fileConfig

from dotenv import load_dotenv
import os

# Load variables from .env *first* so they appear in os.environ
load_dotenv()

from alembic import context
from sqlalchemy import engine_from_config, pool

config = context.config

# Inject the actual DATABASE_URL into Alembic’s in-memory config.
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL is not set – check your .env or shell env")

config.set_main_option("sqlalchemy.url", db_url)
# ── END PATCH ──────────────────────────────────────────────────


config = context.config
# Replace the placeholder sqlalchemy.url in memory with the real value
config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])
# ──────────────────────────────────────────────────────────────────

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model’s MetaData here for autogenerate support
target_metadata = None

# -----------------------------------------------------------------
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
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
