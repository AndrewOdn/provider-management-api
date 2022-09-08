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

DB_LOCAL_HOST = 'localhost'
DB_LOCAL_PORT = 3306
DB_LOCAL_NAME = 'marketplace_new'
DB_LOCAL_USER = 'admin'
DB_LOCAL_PASS = '2001'

engine = create_async_engine(
    f"postgresql+psycopg2://{DB_TEST_USER}:"
    f"{DB_TEST_PASS}@{DB_TEST_HOST}:"
    f"{DB_TEST_PORT}/{DB_TEST_NAME}"
)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)

class Users(Base):
    __tablename__ = "users"
    id = Column(INTEGER, primary_key=True)
    rule_level = Column(SMALLINT, default=1)
    username = Column(VARCHAR(24), primary_key=True)
    password = Column(VARCHAR(24))
    activated = Column(SMALLINT, default=0)


class Tokens(Base):
    __tablename__ = "tokens"
    id = Column(INTEGER, primary_key=True)
    user_id = Column(VARCHAR(24))
    token = Column(VARCHAR(256))


Users.metadata.create_all(engine)
Tokens.metadata.create_all(engine)