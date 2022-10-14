import logging

import bcrypt
import falcon
from falcon import Request, Response
from falcon.media.validators import jsonschema
from src.sql.models import Product, Offer
from src.utils import add_new_refresh, get_new_access, api
from src.schemas.product import update_data_offer, update_offer_200, Product_tag
from src.schemas.base import base401, base500, base_header
from falcon import Request, Response
from spectree import Response as resp
from src.sql.connection import async_session
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from src.sql.on_sql_func import dict_transform


async def async_update_product(filt, user_id):
    async with async_session() as session:
        session.begin()
        for filters in filt:
            product_id = filters['product_id']
            try:
                filters['price'] = float(filters['price'])
            except:
                filters['price'] = 0
            try:
                filters['quantity'] = float(filters['quantity'])
            except:
                filters['quantity'] = 0
            if filters['price'] is None or filters['price'] == '' or filters['price'] == "None":
                filters['price'] = 0
            if filters['quantity'] is None or filters['quantity'] == '' or filters['quantity'] == "None":
                filters['quantity'] = 0
            if filters['price'] != 0 or filters['quantity'] != 0:
                try:
                    upd = await session.execute(
                        f"""UPDATE offers SET price = {filters['price']}, quantity = {filters['quantity']}
WHERE offers.product_id = '{product_id}' AND user_id = {user_id}""")
                except Exception as exp:
                    raise falcon.HTTPNotAcceptable("Нет такого товара в каталоге")
                if upd.rowcount == 0:
                    try:
                        await session.execute(
                            insert(Offer).values(price=filters['price'], quantity=filters['quantity'],
                                                 product_id=product_id, user_id=user_id))
                    except Exception as exp:
                        raise falcon.HTTPNotAcceptable("Нет такого товара в каталоге")
                await session.commit()
            else:
                await session.execute(
                    delete(Offer).where(Offer.user_id == user_id).where(Offer.product_id == product_id))
                await session.commit()
    return {"status": True}


class Update:
    @api.validate(
        json=update_data_offer, resp=resp(HTTP_200=update_offer_200, HTTP_401=base401, HTTP_500=base500),
        tags=[Product_tag], headers=base_header,
    )
    async def on_post(self, req: Request, res: Response):
        """
        Получение информации по магазинам на маркетплейсах
        """
        data = await req.get_media()
        logging.debug("Reached on_post() in Login")
        out = await async_update_product(data, req.context.get("user_id"))
        res.media = out


route = Update()
