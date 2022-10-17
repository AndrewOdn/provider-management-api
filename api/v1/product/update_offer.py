"""
api/v1/product/update_offer route
"""
import logging

import falcon
from falcon import Request, Response
from spectree import Response as resp
from sqlalchemy import delete, insert

from src.schemas.base import Base401, Base500, BaseHeader
from src.schemas.product import Product_tag, UpdateDataOffer, UpdateOffer200
from src.sql.connection import async_session
from src.sql.models import Offer
from src.utils import api


async def async_update_product(filt, user_id):
    """Update/Insert products list func"""
    async with async_session() as session:
        session.begin()
        for filters in filt:
            product_id = filters["product_id"]
            try:
                filters["price"] = float(filters["price"])
            except:
                filters["price"] = 0
            try:
                filters["quantity"] = float(filters["quantity"])
            except:
                filters["quantity"] = 0
            if (
                filters["price"] is None
                or filters["price"] == ""
                or filters["price"] == "None"
            ):
                filters["price"] = 0
            if (
                filters["quantity"] is None
                or filters["quantity"] == ""
                or filters["quantity"] == "None"
            ):
                filters["quantity"] = 0
            if filters["price"] != 0 or filters["quantity"] != 0:
                try:
                    upd = await session.execute(
                        f"""UPDATE offers SET price = {filters['price']},
quantity = {filters['quantity']}
WHERE offers.product_id = '{product_id}' AND user_id = {user_id}"""
                    )
                except Exception:
                    raise falcon.HTTPNotAcceptable("Нет такого товара в каталоге")
                if upd.rowcount == 0:
                    try:
                        await session.execute(
                            insert(Offer).values(
                                price=filters["price"],
                                quantity=filters["quantity"],
                                product_id=product_id,
                                user_id=user_id,
                            )
                        )
                    except Exception as exp:
                        raise falcon.HTTPNotAcceptable("Нет такого товара в каталоге")
                await session.commit()
            else:
                await session.execute(
                    delete(Offer)
                    .where(Offer.user_id == user_id)
                    .where(Offer.product_id == product_id)
                )
                await session.commit()
    return {"status": True}


class Update:
    """update_offer route"""
    @api.validate(
        json=UpdateDataOffer,
        resp=resp(HTTP_200=UpdateOffer200, HTTP_401=Base401, HTTP_500=Base500),
        tags=[Product_tag],
        headers=BaseHeader,
    )
    async def on_post(self, req: Request, res: Response):
        """
        Получение информации по магазинам на маркетплейсах
        """
        data = await req.get_media()
        logging.debug("Reached on_post() in Login")
        out = await async_update_product(data, req.context.get("user_id"))
        res.media = out
        if not data:
            res.media = {"status": False}


route = Update()
