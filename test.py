import asyncio
import sqlalchemy as sa

from aiomysql.sa import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import BIGINT, CHAR, DECIMAL, TEXT, VARCHAR, DateTime, Float

Base = declarative_base()
from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import INTEGER, VARCHAR, SMALLINT
DB_TEST_HOST = 'localhost'
DB_TEST_PORT = 5432
DB_TEST_NAME = 'provider_api'
DB_TEST_USER = 'admin'
DB_TEST_PASS = '2001'

DB_LOCAL_HOST = '2.59.41.170'
DB_LOCAL_PORT = 5432
DB_LOCAL_NAME = 'provider_api'
DB_LOCAL_USER = 'admin'
DB_LOCAL_PASS = '2001'

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

class Users(Base):
    __tablename__ = "users"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    rule_level = Column(SMALLINT, default=1)
    username = Column(VARCHAR(24), primary_key=True)
    password = Column(VARCHAR(256))
    activated = Column(SMALLINT, default=0)


class Tokens(Base):
    __tablename__ = "tokens"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(VARCHAR(24))
    token = Column(VARCHAR(256))


Users.metadata.create_all(engine)
Tokens.metadata.create_all(engine)