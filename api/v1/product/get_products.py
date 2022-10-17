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
            users_only = True
            if "user_offers_only" in filters and filters['user_offers_only'] is bool:
                users_only = filters['user_offers_only']

            out = []
            if users_only:
                query = (
                    f"""SELECT products.id AS id, products.article AS article, products.barcode AS barcode, 
products.name AS name, countries.code AS country_code, countries.emoji AS country_emoji,
countries.id AS country_id,countries.name AS country_name, offers.id AS offer_id, offers.price AS 
offer_price, offers.product_id AS offer_product_id,offers.quantity AS offer_quantity,
offers.user_id AS offer_user_id, offers.updated AS offer_updated,
products.code AS code, products.updated AS updated FROM products
LEFT OUTER JOIN offers ON offers.product_id = products.id AND user_id = {user_id}
LEFT OUTER JOIN countries ON countries.id = products.country_id"""
                )
                prefix = " WHERE "
                if filters:
                    if "country" in filters:
                        query += prefix + f"countries.name = '{filters['country']}'"
                        prefix = " AND "
                    if "id" in filters:
                        query += prefix + f"products.id = '{filters['id']}'"
                        prefix = " AND "
                    if "article" in filters:
                        query += prefix + f"products.article = '{filters['article']}'"
                        prefix = " AND "
                    if "code" in filters:
                        query += prefix + f"products.code = '{filters['code']}'"
                        prefix = " AND "

                result = await session.execute(query)

                for a in result:
                    # if a[12] == user_id:
                    temp = (
                        {
                            "id": a[0],
                            "article": a[1],
                            "barcode": a[2],
                            "name": a[3],
                            "country": {
                                "code": a[4],
                                "emoji": a[5],
                                "id": a[6],
                                "name": a[7],
                            },
                            "code": a[14],
                            "updated": str(a[15]),
                        }
                    )
                    if a[13] and a[9]:
                        temp['offer'] = {
                            "id": a[8],
                            "price": float(a[9]) if a[9] else None,
                            "product_id": a[10],
                            "quantity": a[11],
                            "user_id": a[12],
                            "updated": str(a[13]) if a[13] else None,
                        }
                    out.append(temp)
            else:
                query = (
                    f"SELECT DISTINCT products.id AS id, products.article AS article, products.barcode AS barcode, "
                    f"products.name AS name, countries.code AS country_code, countries.emoji AS country_emoji,"
                    f"countries.id AS country_id,countries.name AS country_name,"
                    f"products.code AS code, products.updated AS updated FROM products "
                    f"JOIN countries ON products.country_id = countries.id"
                )
                prefix = " WHERE "
                if filters:
                    if "country" in filters:
                        query += prefix + f"countries.name = '{filters['country']}'"
                        prefix = " AND "
                    if "id" in filters:
                        query += prefix + f"products.id = '{filters['id']}'"
                        prefix = " AND "
                    if "article" in filters:
                        query += prefix + f"products.article = '{filters['article']}'"
                        prefix = " AND "
                    if "code" in filters:
                        query += prefix + f"products.code = '{filters['code']}'"
                result = await session.execute(query)

                for a in result:
                    out.append(
                        {
                            "id": a[0],
                            "article": a[1],
                            "barcode": a[2],
                            "name": a[3],
                            "country": {
                                "code": a[4],
                                "emoji": a[5],
                                "id": a[6],
                                "name": a[7],
                            },
                            "code": a[8],
                            "updated": str(a[9]),
                        }
                    )
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
