from logging.config import fileConfig
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
import asyncio
import sys
import os

# Добавляем путь к app в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Импортируем ваши модели SQLAlchemy
from app.models import models

# Получаем конфиг из alembic.ini
config = context.config

# Настраиваем логгер
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Устанавливаем target_metadata для автогенерации миграций
target_metadata = models.Base.metadata

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        include_schemas=True
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

asyncio.run(run_migrations_online())
