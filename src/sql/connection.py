"""
Connection declaration
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:" f"{DB_PASS}@{DB_HOST}:" f"{DB_PORT}/{DB_NAME}"
)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
