import logging

import bcrypt
import falcon
from falcon import Request, Response
from falcon.media.validators import jsonschema
from src.sql import Users
from src.utils import add_new_refresh, get_new_access, api
from src.schemas.account import login_200, refresh_200, login_data, Account_tag, login_401
from src.schemas.base import base401, base500, base_header
from falcon import Request, Response
from spectree import Response as resp
from src.sql import Users, async_session
from sqlalchemy.future import select
import sqlalchemy as sa


async def async_check_users(name):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Users).where(Users.username == name))
            for a in result.scalars():
                return {'id': a.id, 'password': a.password, 'rule_level': a.rule_level, 'activated': a.activated}

    return False


class Login:
    @api.validate(
        json=login_data, resp=resp(HTTP_200=login_200, HTTP_401=login_401, HTTP_500=base500), tags=[Account_tag],
    )
    async def on_post(self, req: Request, res: Response):
        """
        Логин
        """
        logging.debug("Reached on_post() in Login")
        data = await req.get_media()
        username = data["username"].lower()
        user = await async_check_users(username)
        if not user or not bcrypt.checkpw(
                data["password"].encode("utf-8"), user["password"].encode("utf-8")
        ):
            raise falcon.HTTPUnauthorized("Неверный логин или пароль")
        if not user.get("activated"):
            raise falcon.HTTPUnauthorized(
                "Ожидайте активации вашего аккаунта администрацией ресурса"
            )
        access = await get_new_access(username, user["id"])
        refresh = await add_new_refresh(username, user["id"])
        res.media = {"accessToken": access, "refreshToken": refresh}


route = Login()
