"""
api/v1/product/favorite/set route
"""
import logging

import falcon
from falcon import Request, Response
from spectree import Response as resp
from sqlalchemy import delete, insert

from src.schemas.base import Base401, Base500, BaseHeader
from src.schemas.product import Product_tag, FavoriteSetData, FavoriteSet200
from src.sql.connection import async_session
from src.sql.models import Offer
from src.utils import api
from src.sql.models import ProductFavourite
from sqlalchemy.exc import IntegrityError


async def async_set_favorite(data, user_id):
    """Insert  favorite products func"""
    async with async_session() as session:
        result = await session.execute(
            f"""SELECT count(*) FROM products_favourites WHERE products_favourites.id = {user_id} and products_favourites.product_id = {data["product_id"]}"""
        )
        for item in result:
            count = item.count
        if count == 0:
            try:
                await session.execute(
                    insert(ProductFavourite).values(
                        user_id=user_id,
                        product_id=str(data["product_id"]),
                    )
                )
                await session.commit()
            except IntegrityError:
                raise falcon.HTTPNotAcceptable("Нет такого товара в каталоге ",
                                               f"{data['product_id']} отсутствует в прайс листе, невозможно добавить в избранное")
    return {"status": True}


class Set:
    """favorite_set route"""

    @api.validate(
        json=FavoriteSetData,
        resp=resp(HTTP_200=FavoriteSet200, HTTP_401=Base401, HTTP_500=Base500),
        tags=[Product_tag],
        headers=BaseHeader,
    )
    async def on_post(self, req: Request, res: Response):
        """
        route's body
        """
        data = await req.get_media()
        logging.debug("Reached on_post() in Login")
        out = await async_set_favorite(data, req.context.get("user_id"))
        res.media = out
        if not data:
            res.media = {"status": False}


route = Set()
