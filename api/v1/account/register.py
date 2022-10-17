"""
api/v1/account/register route
"""

from typing import Dict

import bcrypt
import falcon
import sqlalchemy as sa
from falcon import Request, Response
from spectree import Response as resp
from sqlalchemy.future import select

from src.schemas.account import Account_tag, Register200, Register401, RegisterData
from src.schemas.base import Base500
from src.sql.connection import async_session
from src.sql.models import User
from src.utils import api

# async def test(name):
#     async with async_session() as session:
#         async with session.begin():
#             result = await session.execute(
#                 select(Stone))
#             for a in result.scalars():
#                 j_data = await dict_transform(a.__dict__)
#                 logging.info(str(j_data))
#     return False


async def async_check_users(name):
    """Check information func"""
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.username == name))
            for item in result.scalars():
                return True
    return False


async def async_insert_user(user_data):
    """Add new user func"""
    async with async_session() as session:
        async with session.begin():
            await session.execute(sa.insert(User).values(user_data))
            await session.commit()
    return True


class Register:
    """Register route"""
    @api.validate(
        json=RegisterData,
        resp=resp(HTTP_200=Register200, HTTP_401=Register401, HTTP_500=Base500),
        tags=[Account_tag],
    )
    async def on_post(self, req: Request, res: Response):
        """
        Registration
        """
        data: Dict
        password: str
        data = await req.get_media()
        username = data.get("username").lower()
        if await async_check_users(username):
            raise falcon.HTTPUnauthorized("Пользователь с таким логином уже существует")
        password = data.get("password")
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt(12)
        ).decode("utf-8")
        user_data = {
            "username": username,
            "password": hashed_password,
        }
        user = await async_insert_user(user_data)
        if not user:
            res.status = falcon.HTTP_INTERNAL_SERVER_ERROR
            res.media = {"title": "Внутренняя ошибка сервиса"}
            raise falcon.HTTPInternalServerError("Внутренняя ошибка сервиса")
        res.media = {
            "status": True,
            "title": "Напишите администратору сервиса для активации аккаунта",
        }


route = Register()
