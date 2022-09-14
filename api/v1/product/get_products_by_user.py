import logging

import bcrypt
import falcon
from falcon import Request, Response
from falcon.media.validators import jsonschema
from src.sql.models import Offer
from src.utils import add_new_refresh, get_new_access, api
from src.schemas.product import get_product_by_user_200, get_data_product_by_user, Product_tag
from src.schemas.base import base401, base500, base_header
from falcon import Request, Response
from spectree import Response as resp
from src.sql.connection import async_session
from sqlalchemy.future import select
from src.sql.on_sql_func import dict_transform


async def async_get_product_by_user(filters):
    async with async_session() as session:
        async with session.begin():
            query_user_id = True
            query_product_id = True
            if filters:
                if 'user_id' in filters:
                    query_user_id = Offer.id == filters['user_id']
                if 'product_id' in filters:
                    query_product_id = Offer.article == filters['product_id']
            result = await session.execute(
                select(Offer).where(query_user_id).where(query_product_id))
            out = []
            for a in result.scalars().unique():
                out.append({
                    "id": a.id,
                    "price": float(a.price),
                    "product_id": a.product_id,
                    "quantity": a.quantity,
                    "product": {
                        "id": a.product.id,
                        "article": a.product.article,
                        "barcode": a.product.barcode,
                        "name": a.product.name,
                        "country": {"code": a.product.country.code,
                                    "emoji": a.product.country.emoji,
                                    "id": a.product.country.id,
                                    "name": a.product.country.name},
                        "code": a.product.code,
                        "updated": str(a.product.updated),
                    },
                    "user_id": a.user_id,
                    "updated": str(a.updated),
                })
    return out


class Get:
    @api.validate(
        json=get_data_product_by_user, resp=resp(HTTP_200=get_product_by_user_200, HTTP_401=base401, HTTP_500=base500),
        tags=[Product_tag], headers=base_header,
    )
    async def on_post(self, req: Request, res: Response):
        """
        Получение информации по магазинам на маркетплейсах
        """
        data = await req.get_media()
        logging.debug("Reached on_post() in Login")
        out = await async_get_product_by_user(data)
        res.media = out


route = Get()
