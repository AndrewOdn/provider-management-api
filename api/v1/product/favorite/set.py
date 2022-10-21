"""   /api/v1/product/favorite/set route   """
from src.schemas.product import FavoriteSetData, FavoriteSet200
from fastapi import APIRouter, Body, Depends
from src.middleware import process_resource
from src.methods.product import async_set_favorite

router = APIRouter()


@router.post("/api/v1/product/favorite/set", tags=["Product", "Favorite"], response_model=FavoriteSet200)
async def favorite_set(body: FavoriteSetData = Body(None), JWT: bool = Depends(process_resource)):
    """
    Добавление товара в избранное
    :param body:
    :param JWT:
    :return:
    """
    out = await async_set_favorite(body, JWT['user_id'])
    return out
