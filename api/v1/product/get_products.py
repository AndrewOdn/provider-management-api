import logging

import bcrypt
import falcon
from falcon import Request, Response
from falcon.media.validators import jsonschema
from src.sql.models import Product, Offer
from src.utils import add_new_refresh, get_new_access, api
from src.schemas.product import get_product_200, get_data_product, Product_tag
from src.schemas.base import base401, base500, base_header
from falcon import Request, Response
from spectree import Response as resp
from src.sql.connection import async_session
from sqlalchemy.future import select
from src.sql.on_sql_func import dict_transform


async def async_get_product(filters, user_id):
    async with async_session() as session:
        async with session.begin():
            query_id = True
            query_article = True
            query_country = True
            query_code = True
            if filters:
                if 'id' in filters:
                    query_id = Product.id == filters['id']
                if 'article' in filters:
                    query_article = Product.article == filters['article']
                if 'country' in filters:
                    query_country = Product.country == filters['country']
                if 'code' in filters:
                    query_code = Product.code == filters['code']
                if user_id:
                    result = await session.execute(
                        select(Product, Offer).where(query_id).where(query_article).where(query_country).where(
                            query_code))
                    out = []
                    for a in result.scalars().unique():
                        if 'user_offers_only' in filters:
                            indicator = True
                        else:
                            indicator = False
                        for offer in a.offers:
                            if offer.user_id == filters['user_id']:
                                out.append({
                                    "id": a.id,
                                    "article": a.article,
                                    "barcode": a.barcode,
                                    "name": a.name,
                                    "country": {"code": a.country.code,
                                                "emoji": a.country.emoji,
                                                "id": a.country.id,
                                                "name": a.country.name},
                                    "offer": {"id": offer.id,
                                              "price": float(offer.price),
                                              "product_id": offer.product_id,
                                              "quantity": offer.quantity,
                                              "user_id": offer.user_id,
                                              "updated": str(offer.updated)},
                                    "code": a.code,
                                    "updated": str(a.updated),
                                })
                                indicator = True
                                break
                        if not indicator:
                            out.append({
                                "id": a.id,
                                "article": a.article,
                                "barcode": a.barcode,
                                "name": a.name,
                                "country": {"code": a.country.code,
                                            "emoji": a.country.emoji,
                                            "id": a.country.id,
                                            "name": a.country.name},
                                "code": a.code,
                                "updated": str(a.updated),
                            })
                return out
            result = await session.execute(
                select(Product).where(query_id).where(query_article).where(query_country).where(query_code))
            out = []
            for a in result.scalars().unique():
                out.append({
                    "id": a.id,
                    "article": a.article,
                    "barcode": a.barcode,
                    "name": a.name,
                    "country": {"code": a.country.code,
                                "emoji": a.country.emoji,
                                "id": a.country.id,
                                "name": a.country.name},
                    "code": a.code,
                    "updated": str(a.updated),
                })
    return out


class Get:
    @api.validate(
        json=get_data_product, resp=resp(HTTP_200=get_product_200, HTTP_401=base401, HTTP_500=base500),
        tags=[Product_tag], headers=base_header,
    )
    async def on_post(self, req: Request, res: Response):
        """
        Получение информации по магазинам на маркетплейсах
        """
        data = await req.get_media()
        logging.debug("Reached on_post() in Login")
        out = await async_get_product(data, req.context.get("user_id"))
        res.media = out


route = Get()
