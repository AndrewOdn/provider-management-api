from typing import Dict
import logging
import bcrypt
import falcon
from src.utils import api
from src.schemas.account import register_200, register_401, register_data, Account_tag
from src.schemas.base import base401, base500, base_header
from falcon import Request, Response
from spectree import Response as resp
from src.sql import Users, async_session, Stone, dict_transform
from sqlalchemy.future import select
import sqlalchemy as sa

async def test(name):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Stone))
            for a in result.scalars():
                j_data = await dict_transform(a.__dict__)
                logging.info(str(j_data))
    return False


async def async_check_users(name):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Users).where(Users.username == name))
            for a in result.scalars():
                # logging.info(str(a.__dict__))
                return True
    return False


async def async_insert_user(user_data):
    async with async_session() as session:
        async with session.begin():
            await session.execute(sa.insert(Users).values(
                user_data)
            )
            await session.commit()
    return True


class Register:
    @api.validate(
        json=register_data, resp=resp(HTTP_200=register_200, HTTP_401=register_401, HTTP_500=base500),
        tags=[Account_tag],
    )
    async def on_post(self, req: Request, res: Response):
        """
        Регистрация
        """
        data: Dict
        password: str
        data = await req.get_media()
        username = data.get("username").lower()
        if await async_check_users(username):
            raise falcon.HTTPUnauthorized(
                "Пользователь с таким логином уже существует"
            )
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
        res.media = {"status": True, "title": "Напишите администратору сервиса для активации аккаунта"}


route = Register()
