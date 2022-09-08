

import sqlalchemy as sa
from src.sql import Users


DB_TEST_HOST = '31.172.66.21'
DB_TEST_PORT = 3306
DB_TEST_NAME = 'marketplace_new'
DB_TEST_USER = 'OdnodvortsevAndrey'
DB_TEST_PASS = 'sk*o6j0YO5%'

engine = sa.create_engine(
    f"mysql+pymysql://{DB_TEST_USER}:"
    f"{DB_TEST_PASS}@{DB_TEST_HOST}:"
    f"{DB_TEST_PORT}/{DB_TEST_NAME}"
)
