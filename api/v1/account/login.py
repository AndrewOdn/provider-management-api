"""
api/v1/account/login route
"""
import logging
import bcrypt
import falcon
from falcon import Request, Response
from spectree import Response as resp
from sqlalchemy.future import select

from src.schemas.account import (
    Account_tag,
    Login200,
    Login401,
    LoginData,
)
from src.schemas.base import Base500
from src.sql.connection import async_session
from src.sql.models import User
from src.utils import add_new_refresh, api, get_new_access


async def async_check_users(name):
    """Get user information func"""
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.username == name))
            for item in result.scalars().unique():
                return {
                    "id": item.id,
                    "password": item.password,
                    "rule_level": item.rule_level,
                    "activated": item.activated,
                }

    return False


class Login:
    """Login route"""
    @api.validate(
        json=LoginData,
        resp=resp(HTTP_200=Login200, HTTP_401=Login401, HTTP_500=Base500),
        tags=[Account_tag],
    )
    async def on_post(self, req: Request, res: Response):
        """
        route's body
        """
        logging.debug("Reached on_post() in Login")
        data = await req.get_media()
        username = data["username"]
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
