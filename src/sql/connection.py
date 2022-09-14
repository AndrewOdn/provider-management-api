from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DB_HOST = "31.172.66.21"
DB_PORT = 3306
DB_NAME = "marketplace_new"
DB_USER = "OdnodvortsevAndrey"
DB_PASS = "sk*o6j0YO5%"

DB_LOCAL_HOST = "localhost"
DB_LOCAL_PORT = 5432
DB_LOCAL_NAME = "provider_api"
DB_LOCAL_USER = "admin"
DB_LOCAL_PASS = "2001"

DB_TEST_HOST = "2.59.41.170"
DB_TEST_PORT = 5432
DB_TEST_NAME = "provider_api"
DB_TEST_USER = "admin"
DB_TEST_PASS = "2001"

engine = create_async_engine(
    f"postgresql+asyncpg://{DB_TEST_USER}:"
    f"{DB_TEST_PASS}@{DB_TEST_HOST}:"
    f"{DB_TEST_PORT}/{DB_TEST_NAME}"
)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)