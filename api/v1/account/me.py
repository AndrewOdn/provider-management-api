import logging

import bcrypt
import falcon
import sqlalchemy as sa
from falcon import Request, Response
from falcon.media.validators import jsonschema
from spectree import Response as resp
from sqlalchemy.future import select

from src.schemas.account import Account_tag, me_200, me_data
from src.sql.models import User
from src.sql.connection import async_session
from src.utils import add_new_refresh, api, get_new_access


async def async_get_users(name):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.username == name))
            for a in result.scalars():
                return {"username": a.username}
    return False


class Me:
    @api.validate(
        resp=resp(HTTP_200=me_200),
        tags=[Account_tag],
        deprecated=True,
    )
    async def on_get(self, req: Request, res: Response):
        """
        Получение информации по пользователю

        Deprecated
        """
        logging.info("Reached on_post() in Login")
        username = req.context.get("username")
        user = await async_get_users(username)
        if not user:
            raise falcon.HTTPInternalServerError("Внутренняя ошибка сервиса")
        res.media = {"user": user}


route = Me()
