import sqlalchemy as sa

from src.sql.models import Base

DB_TEST_HOST = "localhost"
DB_TEST_PORT = 5432
DB_TEST_NAME = "provider_api"
DB_TEST_USER = "admin"
DB_TEST_PASS = "2001"

DB_LOCAL_HOST = "2.59.41.170"
DB_LOCAL_PORT = 5432
DB_LOCAL_NAME = "provider_api"
DB_LOCAL_USER = "admin"
DB_LOCAL_PASS = "2001"

engine = sa.create_engine(
    f"postgresql+psycopg2://{DB_LOCAL_USER}:"
    f"{DB_LOCAL_PASS}@{DB_LOCAL_HOST}:"
    f"{DB_LOCAL_PORT}/{DB_LOCAL_NAME}"
)
session = sa.orm.Session(
    bind=engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=True,
    info=None,
)
Base.metadata.create_all(engine)
