import logging
import time
from datetime import datetime, timedelta
from typing import Dict

import jwt
from spectree import SpecTree

from config import ACCESS_SECRET, REFRESH_SECRET, TIKEN_LIFE_IN_SECONDS

API_TOKEN = "<api_token>"
api = SpecTree(
    "falcon-asgi",
    title="Marketplaces api service",
    version="0.0.1",
)

import sqlalchemy as sa

from .sql.models import Token
from .sql.connection import async_session


async def async_add_token(data):
    async with async_session() as session:
        async with session.begin():
            await session.execute(sa.insert(Token).values(data))
            await session.commit()
    return False


async def add_new_refresh(username: str, user_id: int) -> Dict:
    logging.debug(f"Added new refresh: {username}")
    token = jwt.encode(
        {
            "username": username,
            "user_id": user_id,
            "created": int(time.time() * 1000),
        },
        REFRESH_SECRET,
        algorithm="HS256",
    )
    await async_add_token({"user_id": user_id, "token": token})
    return token


async def get_new_access(username: str, user_id: int) -> Dict:
    logging.debug(f"Get new access: {username}")
    token = jwt.encode(
        {
            "username": username,
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(seconds=TIKEN_LIFE_IN_SECONDS),
        },
        ACCESS_SECRET,
        algorithm="HS256",
    )
    return token


async def token_is_valid(token: str, secret: str):
    try:
        return jwt.decode(
            token.split(" ")[-1],
            secret,
            verify="True",
            algorithms=["HS256"],
            options={"verify_exp": True},
        )
    except (jwt.DecodeError, jwt.ExpiredSignatureError) as err:
        logging.debug("Token validation failed Error :{}".format(str(err)))
        return False
