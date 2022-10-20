"""
api/v1/product/update_offer route
"""
import logging

from falcon import Request, Response
from spectree import Response as resp
from sqlalchemy import delete

from src.schemas.base import Base401, Base500, BaseHeader
from src.schemas.product import Product_tag, FavoriteRemoteData, FavoriteRemote200
from src.sql.connection import async_session
from src.sql.models import ProductFavourite
from src.utils import api


async def async_remove_favorite(data, user_id):
    """Delete favorite products func"""
    async with async_session() as session:
        await session.execute(
            delete(ProductFavourite)
                .where(ProductFavourite.user_id == user_id)
                .where(ProductFavourite.product_id == data['product_id'])
        )
        await session.commit()
    return {"status": True}


class Remove:
    """favorite_remote route"""

    @api.validate(
        json=FavoriteRemoteData,
        resp=resp(HTTP_200=FavoriteRemote200, HTTP_401=Base401, HTTP_500=Base500),
        tags=[Product_tag],
        headers=BaseHeader,
    )
    async def on_post(self, req: Request, res: Response):
        """
        route's body
        """
        data = await req.get_media()
        logging.debug("Reached on_post() in Login")
        out = await async_remove_favorite(data, req.context.get("user_id"))
        res.media = out
        if not data:
            res.media = {"status": False}


route = Remove()
