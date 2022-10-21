"""   /api/v1/account/register route   """

from fastapi import APIRouter, Body, HTTPException
import bcrypt
from src.schemas.account import (Register200, RegisterData)
from src.methods.account import async_check_users, async_insert_user

router = APIRouter()


@router.post("/api/v1/account/register", tags=["Account"], response_model=Register200)
async def registration(body: RegisterData = Body(None)):
    """
    Регистрация пользователей
    :param body:
    :return:
    """
    raise HTTPException(500, "Регистрация временно недоступна")
    username = body.username.lower()
    if await async_check_users(username):
        raise HTTPException(401, "Пользователь с таким логином уже существует")
    password = body.password
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt(12)
    ).decode("utf-8")
    user_data = {
        "username": username,
        "password": hashed_password,
    }
    user = await async_insert_user(user_data)
    if not user:
        raise HTTPException(500, "Внутренняя ошибка сервиса")
    return {
        "status": True,
        "detail": "Напишите администратору сервиса для активации аккаунта",
    }
