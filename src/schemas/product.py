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
    id: str = None
    name: str = None


class GetDataProduct(BaseModel):
    """api/v1/product/get_products request validation model"""

    user_offers_only: Optional[bool] = False
    id: Optional[str] = None
    article: Optional[str] = None
    country: Optional[str] = None
    code: Optional[str] = None


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

    id: str
    article: str
    barcode: str = None
    name: str
    offer: Optional[ProductElementTwo]
    country: ProductCountry
    code: str = None
    updated: constr(
        regex=r"202\d{1}-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01]) "
        r"([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])\.\d{6}\+\d{2}\:\d{2}$"
    )


class GetProduct200(BaseModel):
    """api/v1/product/get_products http200 response validation model"""

    __root__: List[ProductPartOne]


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
