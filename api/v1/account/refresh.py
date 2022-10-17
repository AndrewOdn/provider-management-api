"""
api/v1/account/refresh route
"""
import logging
import falcon
from falcon import Request, Response
from spectree import Response as resp
from sqlalchemy.future import select

from config import REFRESH_SECRET
from src.schemas.account import Account_tag, Refresh200, Refresh401, RefreshData
from src.schemas.base import Base500
from src.sql.connection import async_session
from src.sql.models import Token, User
from src.utils import add_new_refresh, api, get_new_access, token_is_valid


async def async_check_user_tokens(token):
    """Check token's availability for user"""
    async with async_session() as session:
        async with session.begin():
            result_one = await session.execute(
                select(Token).where(Token.token == token)
            )
            for item in result_one.scalars().unique():
                return True
    return False


class Refresh:
    """Refresh route"""
    @api.validate(
        json=RefreshData,
        resp=resp(HTTP_200=Refresh200, HTTP_401=Refresh401, HTTP_500=Base500),
        tags=[Account_tag],
    )
    async def on_post(self, req: Request, res: Response):
        """
        Refresh token
        """
        logging.debug("Reached on_post() in Refresh")
        data = await req.get_media()
        refresh_token = data["refreshToken"]
        refresh_token_data = await token_is_valid(refresh_token, REFRESH_SECRET)
        if refresh_token_data:
            username = refresh_token_data["username"]
            user_id = refresh_token_data["user_id"]
            user = await async_check_user_tokens(refresh_token)
            if not user:
                raise falcon.HTTPUnauthorized(
                    "Нет такого пользователя или неверный токен"
                )
            access = await get_new_access(username, user_id)
            refresh = await add_new_refresh(username, user_id)
            res.media = {"accessToken": access, "refreshToken": refresh}
        else:
            raise falcon.HTTPUnauthorized("Нет такого пользователя или неверный токен")


route = Refresh()
