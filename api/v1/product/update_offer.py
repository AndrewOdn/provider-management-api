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
from sqlalchemy.exc import IntegrityError

async def async_update_product(filt, user_id):
    """Update/Insert products list func"""
    async with async_session() as session:
        session.begin()
        result = await session.execute(
            f"""SELECT partner_id FROM users WHERE users.id = {user_id}"""
        )
        for item in result:
            partner_id = item.partner_id
        for filters in filt:
            product_id = str(filters["product_id"])
            filters["price"] = float(filters["price"]) if filters["price"] and filters["price"] != "" else 0
            filters["quantity"] = float(filters["quantity"]) if filters["quantity"] and filters["quantity"] != "" else 0
            if filters["price"] != 0 or filters["quantity"] != 0:
                try:
                    upd = await session.execute(
                        f"""UPDATE offers SET price = {filters['price']},
    quantity = {filters['quantity']}
    WHERE offers.product_id = '{product_id}' AND offers.partner_id = {partner_id}"""
                    )
                except IntegrityError:
                    raise falcon.HTTPNotAcceptable("Нет такого товара в каталоге ",
                                                   f"{product_id} отсутствует в прайс листе, невозможно выставить на него цену")
                if upd.rowcount == 0:
                    try:
                        await session.execute(
                            insert(Offer).values(
                                price=filters["price"],
                                quantity=filters["quantity"],
                                product_id=product_id,
                                partner_id=partner_id,
                            )
                        )
                    except IntegrityError:
                        raise falcon.HTTPNotAcceptable("Нет такого товара в каталоге ", f"{product_id} отсутствует в прайс листе, невозможно выставить на него цену")
                    # raise falcon.HTTPNotAcceptable("Нет такого товара в каталоге")
                await session.commit()
            else:
                await session.execute(
                    delete(Offer)
                    .where(Offer.partner_id == partner_id)
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
