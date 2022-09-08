import logging

import bcrypt
import falcon
from falcon import Request, Response
from falcon.media.validators import jsonschema
from src.sql import Users
from src.utils import add_new_refresh, get_new_access
from src.utils import api
from src.schemas.account import me_200, me_data, Account_tag
from falcon import Request, Response
from spectree import Response as resp
from src.sql import Users, async_session, dict_transform, Stone
from sqlalchemy.future import select
import sqlalchemy as sa

async def async_get_users(name):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Users).where(Users.username == name))
            for a in result.scalars():
                return {'username': a.username}
    return False


class Me:
    @api.validate(
        resp=resp(HTTP_200=me_200), tags=[Account_tag],deprecated=True,
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
