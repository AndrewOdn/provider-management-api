"""   /api/v1/account/me route   """
from fastapi import APIRouter, HTTPException, Depends, Request
from src.middleware import process_resource
from src.schemas.account import Me200
from src.methods.account import async_get_users

router = APIRouter()


@router.get("/api/v1/account/me", tags=["Account"], response_model=Me200)
async def me(request: Request, JWT: bool = Depends(process_resource)):
    """
    Информация по аккаунту
    :param request:
    :param JWT:
    :return:
    """
    user = await async_get_users(JWT['user_id'])
    if not user:
        raise HTTPException(500, "Внутренняя ошибка сервиса")
    return user
