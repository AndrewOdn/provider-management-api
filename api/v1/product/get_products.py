"""
api/v1/product/get_products route
"""
from decimal import Decimal
import logging
import json
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
            res = {'data': []}
            query = f"""SELECT users.username AS Username, partners.name AS partner_name, segments.name AS segment_name,
countries.name AS countries_name, countries.emoji AS countries_emoji, countries.code AS countries_code, segments.id AS segment_id,
categories.name AS categories_name,categories.id AS categories_id, brands.name AS brands_name, brands.id AS brands_id, 
products.article AS product_article, products.barcode AS product_barcode, products.name AS product_name,
products.updated AS product_updated, products.id AS product_id,
offers.price AS offer_price, offers.quantity AS offer_quantity, offers.updated AS offer_updated FROM users
LEFT OUTER JOIN partners ON users.partner_id = partners.id AND users.id = {user_id}
LEFT OUTER JOIN partners_segments ON partners_segments.partner_id = partners.id
LEFT OUTER JOIN segments ON partners_segments.segment_id = segments.id
LEFT OUTER JOIN products ON products.segment_id = segments.id
LEFT OUTER JOIN brands ON products.brand_id = brands.id
LEFT OUTER JOIN categories ON products.category_id = categories.id
LEFT OUTER JOIN countries ON products.country_id = countries.id
LEFT OUTER JOIN offers ON products.id = offers.product_id AND offers.partner_id = users.partner_id"""
            prefix = " WHERE "
            if filters:
                # if "partner_name" in filters:
                #     query += prefix + f"partners.name = '{filters['partner_name']}'"
                #     prefix = " AND "
                if "segment_name" in filters:
                    query += prefix + f"segments.name = '{filters['segment_name']}'"
                    prefix = " AND "
                if "category_name" in filters:
                    query += prefix + f"categories.name = '{filters['category_name']}'"
                    prefix = " AND "
                if "brand_name" in filters:
                    query += prefix + f"brands.name = '{filters['brand_name']}'"
                    prefix = " AND "
                if "product_article" in filters:
                    query += prefix + f"products.article = '{filters['product_article']}'"
                    prefix = " AND "
                if "product_barcode" in filters:
                    query += prefix + f"products.barcode = '{filters['product_barcode']}'"
                    prefix = " AND "
                if "product_name" in filters:
                    query += prefix + f"products.name = '{filters['product_name']}'"
                    prefix = " AND "
                # if "product_code" in filters:
                #     query += prefix + f"products.code = '{filters['product_code']}'"
                #     prefix = " AND "
                if "offer_price_asc" in filters:
                    query += prefix + f"offers.price >= '{filters['offer_price_asc']}'"
                    prefix = " AND "
                if "offer_price_desc" in filters:
                    query += prefix + f"offers.price <= '{filters['offer_price_desc']}'"
                    prefix = " AND "
                if "offer_quantity_asc" in filters:
                    query += prefix + f"offers.quantity >= '{filters['offer_quantity_asc']}'"
                    prefix = " AND "
                if "offer_quantity_desc" in filters:
                    query += prefix + f"offers.quantity <= '{filters['offer_quantity_desc']}'"
                    prefix = " AND "
                if "countries_name" in filters:
                    query += prefix + f"countries.name = '{filters['countries_name']}'"
                    prefix = " AND "
                if "countries_code" in filters:
                    query += prefix + f"countries.code = '{filters['countries_code']}'"
                    prefix = " AND "
                if "countries_emoji" in filters:
                    query += prefix + f"countries.emoji = '{filters['countries_emoji']}'"
                    prefix = " AND "
                if "segment_id" in filters:
                    query += prefix + f"segments.id = '{filters['segment_id']}'"
                    prefix = " AND "
                if "brand_id" in filters:
                    query += prefix + f"brands.id = '{filters['brand_id']}'"
                    prefix = " AND "
                if "category_id" in filters:
                    query += prefix + f"categories.id= '{filters['category_id']}'"
                    prefix = " AND "
                if "product_id" in filters:
                    query += prefix + f"products.id = '{filters['product_id']}'"
                    prefix = " AND "

                if "search" in filters:
                    query += prefix + f"segments.name LIKE '%{filters['search']}%' or brands.name LIKE '%{filters['search']}%' or categories.name LIKE '%{filters['search']}%' or products.name LIKE '%{filters['search']}%' or products.id LIKE '%{filters['search']}%' or products.article LIKE '%{filters['search']}%'"
                    prefix = " AND "
                # if "favorite" in filters:
                #     query += prefix + f"products.id = '{filters['product_id']}'"
                #     prefix = " AND "
                if "have_price" in filters:
                    if filters['have_price'] is True:
                        query += prefix + "offers.price > 0"
                    else:
                        query += prefix + "(offers.price = 0 or offers.price is null)"
                    prefix = " AND "
            if 'page' not in filters:
                filters['page'] = 0
            if 'page_size' not in filters:
                filters['page_size'] = 20
            query += f""" OFFSET {filters['page'] * filters['page_size']}
                         LIMIT {filters['page_size']}"""

            result = await session.execute(query)

            for item in result:
                output = {
                    # "username": item.username,
                    # "partner_name": item.partner_name,
                    "segment": {"id": item.segment_id, "name": item.segment_name},
                    "brand": {"id": item.brands_id, "name": item.brands_name},
                    "category": {"id": item.categories_id, "name": item.categories_name},
                    "product": {
                        "id": item.product_id,
                        "article": item.product_article,
                        "barcode": item.product_barcode,
                        "name": item.product_name,
                        "favourite": False,
                        "updated": str(item.product_updated),
                    },
                    "offer": {
                        "price": float(item.offer_price) if item.offer_price else None,
                        "quantity": item.offer_quantity,
                        "updated": str(item.offer_updated) if item.offer_updated else None,
                    },
                    "country": {
                        "code": item.countries_code,
                        "emoji": item.countries_emoji,
                        "name": item.countries_name,
                    },
                }
                res['data'].append(output)
    query = query[query.find('LEFT OUTER JOIN partners'):query.find(' OFFSET')]
    query = "SELECT COUNT(products.id) FROM users " + query
    result = await session.execute(query)
    for item in result:
        total = item.count
    res['page'] = filters['page'] + 1
    res['page_size'] = filters['page_size']
    res['total'] = total
    return res


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
        route's body
        """
        data = await req.get_media()
        logging.debug("Reached on_post() in Login")
        out = await async_get_product(data, req.context.get("user_id"))
        res.media = out


route = Get()
