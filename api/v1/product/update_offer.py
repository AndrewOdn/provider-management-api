"""   /api/v1/product/update_offer route   """
import logging
from src.schemas.product import UpdateDataOffer, UpdateOffer200
from src.methods.product import async_update_product
from fastapi import APIRouter, Body, Depends
from src.middleware import process_resource
router = APIRouter()


@router.post("/api/v1/product/update_offer", tags=["Product"], response_model=UpdateOffer200)
async def update_offer(body: UpdateDataOffer = Body(None), JWT: bool = Depends(process_resource)):
    """
    Обновление цен/кол-ва на предложение по товару
    :param body:
    :param JWT:
    :return:
    """
    logging.debug("Reached on_post() in Login")
    out = await async_update_product(body.__root__, JWT['user_id'])
    return out
