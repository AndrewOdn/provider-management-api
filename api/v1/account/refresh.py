"""   /api/v1/account/refresh route   """
from fastapi import APIRouter, Body, HTTPException
from config import REFRESH_SECRET
from src.schemas.account import (Refresh200, RefreshData)
from src.utils import add_new_refresh, get_new_access, token_is_valid
from src.methods.account import async_check_user_tokens

router = APIRouter()


@router.post("/api/v1/account/refresh", tags=["Account"], response_model=Refresh200)
async def refresh(body: RefreshData = Body(None)):
    """
    Обновление токена
    :param body:
    :return:
    """
    refresh_token = body.refreshToken
    refresh_token_data = await token_is_valid(refresh_token, REFRESH_SECRET)
    if refresh_token_data:
        username = refresh_token_data["username"]
        user_id = refresh_token_data["user_id"]
        user = await async_check_user_tokens(refresh_token)
        if not user:
            raise HTTPException(401, "Нет такого пользователя или неверный токен")
        access = await get_new_access(username, user_id)
        refresh_func = await add_new_refresh(username, user_id)
        return {"accessToken": access, "refreshToken": refresh_func}
    else:
        raise HTTPException(401, "Нет такого пользователя или неверный токен")
