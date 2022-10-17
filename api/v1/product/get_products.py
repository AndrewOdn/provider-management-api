"""
api/v1/product/get_products route
"""
import logging

from falcon import Request, Response
from spectree import Response as resp

from src.schemas.base import Base401, Base500, BaseHeader
from src.schemas.product import GetDataProduct, GetProduct200, Product_tag
from src.sql.connection import async_session
from src.utils import api


async def async_get_product(filters, user_id):
    """Get products and offers list by filters func"""
    async with async_session() as session:
        async with session.begin():
            users_only = True
            if "user_offers_only" in filters and filters["user_offers_only"] is bool:
                users_only = filters["user_offers_only"]

            out = []
            if users_only:
                query = f"""SELECT products.id AS id, products.article AS article,
                            products.barcode AS barcode, products.name AS name, countries.code AS country_code,
                            countries.emoji AS country_emoji, countries.id AS country_id,
                            countries.name AS country_name, offers.id AS offer_id, offers.price AS 
                            offer_price, offers.product_id AS offer_product_id,offers.quantity AS offer_quantity,
                            offers.user_id AS offer_user_id, offers.updated AS offer_updated,
                            products.code AS code, products.updated AS updated FROM products
                            LEFT OUTER JOIN offers ON offers.product_id = products.id AND user_id = {user_id}
                            LEFT OUTER JOIN countries ON countries.id = products.country_id"""
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

                for item in result:
                    # if a[12] == user_id:
                    temp = {
                        "id": item[0],
                        "article": item[1],
                        "barcode": item[2],
                        "name": item[3],
                        "country": {
                            "code": item[4],
                            "emoji": item[5],
                            "id": item[6],
                            "name": item[7],
                        },
                        "code": item[14],
                        "updated": str(item[15]),
                    }
                    if item[13] and item[9]:
                        temp["offer"] = {
                            "id": item[8],
                            "price": float(item[9]) if item[9] else None,
                            "product_id": item[10],
                            "quantity": item[11],
                            "user_id": item[12],
                            "updated": str(item[13]) if item[13] else None,
                        }
                    out.append(temp)
            else:
                query = """SELECT DISTINCT products.id AS id, products.article AS article,
                    products.barcode AS barcode, products.name AS name,
                    countries.code AS country_code, countries.emoji AS country_emoji,
                    countries.id AS country_id,countries.name AS country_name,
                    products.code AS code, products.updated AS updated FROM products 
                    JOIN countries ON products.country_id = countries.id"""

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

                for item in result:
                    out.append(
                        {
                            "id": item[0],
                            "article": item[1],
                            "barcode": item[2],
                            "name": item[3],
                            "country": {
                                "code": item[4],
                                "emoji": item[5],
                                "id": item[6],
                                "name": item[7],
                            },
                            "code": item[8],
                            "updated": str(item[9]),
                        }
                    )
    return out


class Get:
    """get_products route"""
    @api.validate(
        json=GetDataProduct,
        resp=resp(HTTP_200=GetProduct200, HTTP_401=Base401, HTTP_500=Base500),
        tags=[Product_tag],
        headers=BaseHeader,
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
