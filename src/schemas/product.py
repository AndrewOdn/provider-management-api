"""
Pydantic models for api/v1/product routes
"""
from typing import List, Optional, Union

from pydantic import BaseModel, constr
from spectree import Tag

Product_tag = Tag(name="Product", description="ヽ༼ ຈل͜ຈ༼ ▀̿̿Ĺ̯̿̿▀̿ ̿༽Ɵ͆ل͜Ɵ͆ ༽ﾉ")


class ProductCountry(BaseModel):
    """Countries table schema validation model"""

    code: str = None
    emoji: str = None
    name: str = None


class ProductProduct(BaseModel):
    """Countries table schema validation model"""

    article: str = None
    barcode: str = None
    name: str = None
    code: str = None
    updated: str = None


class ProductOffer(BaseModel):
    """Countries table schema validation model"""

    price: str = None
    quantity: int = None


class GetDataProduct(BaseModel):
    """api/v1/product/get_products request validation model"""
    countries_emoji: Optional[str] = None
    countries_code: Optional[int] = None
    countries_name: Optional[str] = None
    offer_quantity: Optional[int] = None
    offer_price: Optional[float] = None
    product_name: Optional[str] = None
    product_barcode: Optional[str] = None
    product_article: Optional[str] = None
    brand_name: Optional[str] = None
    category_name: Optional[str] = None
    segment_name: Optional[str] = None
    partner_name: Optional[str] = None
    product_code: Optional[str] = None
    page_size: Optional[int] = None
    page: Optional[int] = None


# class ProductByUserElementTwo(BaseModel):
#     id: str
#     article: str
#     barcode: str
#     name: str
#     country: ProductCountry
#     code: str
#     updated: constr(
#         regex=r"202\d{1}-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01]) "
#               r"([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])\.\d{6}\+\d{2}\:\d{2}$"
#     )


# class ProductByUserPartOne(BaseModel):
#     user_id: int
#     updated: constr(
#         regex=r"202\d{1}-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01]) "
#               r"([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])\.\d{6}\+\d{2}\:\d{2}$"
#     )
#     id: int
#     price: float
#     product_id: str
#     quantity: int
#     product: ProductByUserElementTwo


class ProductElementTwo(BaseModel):
    """GetProduct200 part"""

    user_id: int
    updated: constr(
        regex=r"202\d{1}-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01]) "
              r"([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])\.\d{6}\+\d{2}\:\d{2}$"
    )
    id: int
    price: float
    product_id: str
    quantity: int


class ProductPartOne(BaseModel):
    """GetProduct200 part"""

    username: str = None
    partner_name: str = None
    segment_name: str = None
    category_name: str = None
    brand_name: str = None
    product: ProductProduct
    offer: ProductOffer
    country: ProductCountry


class GetProduct200(BaseModel):
    """api/v1/product/get_products http200 response validation model"""

    __root__: List[ProductPartOne]
    page: int = None
    page_size: int = None

# class GetProductByUser200(BaseModel):
#     __root__: List[ProductByUserPartOne]


# class GetDataProductByUser(BaseModel):
#     id: Optional[str] = None
#     article: Optional[str] = None
#     country: Optional[str] = None
#     code: Optional[str] = None


class UpdateOffer200(BaseModel):
    """api/v1/product/update_offer http200 response validation model"""

    status: Union[bool, str]


class UpdateDataOfferPart(BaseModel):
    """UpdateDataOffer part"""

    product_id: str
    price: Union[float, str] = None
    quantity: Union[int, str] = None


class UpdateDataOffer(BaseModel):
    """api/v1/product/update_offer request validation model"""

    __root__: List[UpdateDataOfferPart]
