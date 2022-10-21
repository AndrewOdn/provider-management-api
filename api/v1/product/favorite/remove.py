"""   /api/v1/product/favorite/remove route    """
from src.schemas.product import FavoriteRemoteData, FavoriteRemote200
from fastapi import APIRouter, Body, Depends
from src.middleware import process_resource
from src.methods.product import async_remove_favorite
router = APIRouter()


@router.post("/api/v1/product/favorite/remove", tags=["Product", "Favorite"], response_model=FavoriteRemote200)
async def update_offer(body: FavoriteRemoteData = Body(None), JWT: bool = Depends(process_resource)):
    """
    Удаление товара из избранного
    :param body:
    :param JWT:
    :return:
    """
    out = await async_remove_favorite(body, JWT['user_id'])
    return out
