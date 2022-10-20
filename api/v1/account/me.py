"""
api/v1/account/me route
"""
import logging
import falcon
from falcon import Request, Response
from spectree import Response as resp
from sqlalchemy.future import select

from src.schemas.account import Account_tag, Me200
from src.sql.connection import async_session
from src.sql.models import User
from src.utils import api


async def async_get_users(name):
    """Get user information each self func"""
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.username == name))
            for item in result.scalars():
                return {"username": item.username}
    return False


class Me:
    """Me route"""
    @api.validate(
        resp=resp(HTTP_200=Me200),
        tags=[Account_tag],
        deprecated=True,
    )
    async def on_get(self, req: Request, res: Response):
        """
        route's body

        Deprecated
        """
        logging.info("Reached on_post() in Login")
        username = req.context.get("username")
        user = await async_get_users(username)
        if not user:
            raise falcon.HTTPInternalServerError("Внутренняя ошибка сервиса")
        res.media = {"user": user}


route = Me()
