"""
api/v1/order/get_order route, now might be deprecated
"""
import logging
from falcon import Request, Response
from spectree import Response as resp
from sqlalchemy.future import select

from src.schemas.base import Base401, Base500, BaseHeader
from src.schemas.product import Product_tag, GetDataProduct, GetProduct200
from src.sql.connection import async_session
from src.sql.models import Product
from src.utils import api


async def async_get_order(filters):
    """Get order list by filters func"""
    async with async_session() as session:
        async with session.begin():
            query_id = True
            query_article = True
            query_country = True
            query_code = True
            if filters:
                if "id" in filters:
                    query_id = Product.id == filters["id"]
                if "article" in filters:
                    query_article = Product.article == filters["article"]
                if "country" in filters:
                    query_country = Product.country == filters["country"]
                if "code" in filters:
                    query_code = Product.code == filters["code"]
            result = await session.execute(
                select(Product)
                .where(query_id)
                .where(query_article)
                .where(query_country)
                .where(query_code)
            )
            out = []
            for item in result.scalars():
                out.append(
                    {
                        "id": item.id,
                        "article": item.article,
                        "barcode": item.barcode,
                        "name": item.name,
                        "country": item.country,
                        "code": item.code,
                        "updated": str(item.updated),
                    }
                )
    return out


class Get:
    """Get_order route"""
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
        out = await async_get_order(data)
        res.media = out


route = Get()
