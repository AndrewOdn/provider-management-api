from pydantic import BaseModel, Field, constr
from spectree import Tag
from typing import List, Literal, Optional, Dict, Union
from datetime import datetime

Product_tag = Tag(name="Product", description="ヽ༼ ຈل͜ຈ༼ ▀̿̿Ĺ̯̿̿▀̿ ̿༽Ɵ͆ل͜Ɵ͆ ༽ﾉ")


class product_country(BaseModel):
    code: str
    emoji: str
    id: str
    name: str


class get_data_product(BaseModel):
    user_offers_only: Optional[bool] = False
    id: Optional[str] = None
    article: Optional[str] = None
    country: Optional[str] = None
    code: Optional[str] = None


class product_by_user_element_second(BaseModel):
    id: str
    article: str
    barcode: str
    name: str
    country: product_country
    code: str
    updated: constr(regex=
                    r"202\d{1}-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01]) ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])\.\d{6}\+\d{2}\:\d{2}$")


class product_by_user_element_first(BaseModel):
    user_id: int
    updated: constr(
        regex=r"202\d{1}-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01]) ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])\.\d{6}\+\d{2}\:\d{2}$")
    id: int
    price: float
    product_id: str
    quantity: int
    product: product_by_user_element_second


class product_element_first(BaseModel):
    user_id: int
    updated: constr(
        regex=r"202\d{1}-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01]) ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])\.\d{6}\+\d{2}\:\d{2}$")
    id: int
    price: float
    product_id: str
    quantity: int


class product_element(BaseModel):
    id: str
    article: str
    barcode: str
    name: str
    offer: Optional[product_element_first]
    country: product_country
    photo:str
    code: str
    updated: constr(regex=
                    r"202\d{1}-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01]) ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])\.\d{6}\+\d{2}\:\d{2}$")


class get_product_200(BaseModel):
    __root__: List[product_element]


class get_product_by_user_200(BaseModel):
    __root__: List[product_by_user_element_first]


class get_data_product_by_user(BaseModel):
    id: Optional[str] = None
    article: Optional[str] = None
    country: Optional[str] = None
    code: Optional[str] = None


class update_offer_200(BaseModel):
    status: Union[bool, str]


class update_data_offer(BaseModel):
    product_id: str
    price: float
    quantity: int
