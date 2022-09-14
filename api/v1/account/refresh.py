import logging

import bcrypt
import falcon
import sqlalchemy as sa
from falcon import Request, Response
from falcon.media.validators import jsonschema
from spectree import Response as resp
from sqlalchemy.future import select

from config import REFRESH_SECRET
from src.schemas.account import (Account_tag, refresh_200, refresh_401,
                                 refresh_data)
from src.schemas.base import base401, base500, base_header
from src.sql.models import User, Token
from src.sql.connection import async_session
from src.utils import add_new_refresh, api, get_new_access, token_is_valid


async def async_check_user_tokens(name, token, id):
    async with async_session() as session:
        async with session.begin():
            result_one = await session.execute(
                select(Token).where(Token.user_id == id).where(Token.token == token)
            )
            result_two = await session.execute(
                select(User).where(User.username == name).where(User.id == id)
            )
            for a1 in result_one.scalars().unique():
                for a2 in result_two.scalars().unique():
                    return True
    return False


class Refresh:
    @api.validate(
        json=refresh_data,
        resp=resp(HTTP_200=refresh_200, HTTP_401=refresh_401, HTTP_500=base500),
        tags=[Account_tag],
    )
    async def on_post(self, req: Request, res: Response):
        """
        Рефреш токена
        """
        logging.debug("Reached on_post() in Refresh")
        data = await req.get_media()
        refresh_token = data["refreshToken"]
        refresh_token_data = await token_is_valid(refresh_token, REFRESH_SECRET)
        if refresh_token_data:
            username = refresh_token_data["username"]
            user_id = refresh_token_data["user_id"]
            user = await async_check_user_tokens(username, refresh_token, user_id)
            if not user:
                raise falcon.HTTPUnauthorized("Нет такого пользователя или неверный токен")
            access = await get_new_access(username, user_id)
            refresh = await add_new_refresh(username, user_id)
            res.media = {"accessToken": access, "refreshToken": refresh}
        else:
            raise falcon.HTTPUnauthorized("Нет такого пользователя или неверный токен")


route = Refresh()
