"""   /api/v1/account/login route   """
from fastapi import APIRouter, Body, HTTPException
import bcrypt
from src.utils import get_new_access, add_new_refresh
from src.schemas.account import LoginData, Login200
from src.methods.account import async_check_users


router = APIRouter()


@router.post("/api/v1/account/login", tags=["Account"], response_model=Login200)
async def login(body: LoginData = Body(None)):
    """
    login users
    :param body:
    :return:
    """
    username = body.username
    user = await async_check_users(username)
    if not user or not bcrypt.checkpw(
            body.password.encode("utf-8"), user["password"].encode("utf-8")
    ):
        raise HTTPException(401, "Неверный логин или пароль")
    if not user.get("activated"):
        raise HTTPException(401, "Ожидайте активации вашего аккаунта администрацией ресурса")
    access = await get_new_access(username, user["id"])
    refresh = await add_new_refresh(username, user["id"])
    return {"accessToken": access, "refreshToken": refresh}
