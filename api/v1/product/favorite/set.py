"""
api/v1/product/update_offer route
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


async def async_set_favorite(data, user_id):
    """Insert  favorite products func"""
    async with async_session() as session:
        await session.execute(
            insert(ProductFavourite).values(
                user_id=user_id,
                product_id=data["product_id"],
            )
        )
        await session.commit()
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
