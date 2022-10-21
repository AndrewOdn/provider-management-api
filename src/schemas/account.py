"""
Pydantic models for api/v1/account routes
"""
from typing import Literal

from pydantic import BaseModel, constr
from spectree import Tag

Account_tag = Tag(name="Аккаунт", description="🧾🧾")


class Register200(BaseModel):
    """api/v1/account/register http200 response validation model"""
    status: bool
    title: str = "Напишите администратору сервиса для активации аккаунта"


class Register401(BaseModel):
    """api/v1/account/register http401 response validation model"""
    title: str = "Пользователь с таким логином уже существует"


class RegisterData(BaseModel):
    """api/v1/account/register request validation model"""
    username: constr(
        max_length=24, min_length=6, regex=r"^[a-zA-Z]+([_-]?[a-zA-Z0-9])*$"
    )
    password: constr(
        max_length=24, min_length=8, regex=r"^(?=.*\d)(?=.*[a-zA-Z])[a-zA-Z0-9]{7,}$"
    )


class Login200(BaseModel):
    """api/v1/account/login http200 response validation model"""
    accessToken: str
    refreshToken: str


class LoginData(BaseModel):
    """api/v1/account/login request validation model"""
    username: constr(
        max_length=24, min_length=6, regex=r"^[a-zA-Z]+([_-]?[a-zA-Z0-9])*$"
    )
    password: constr(
        max_length=24, min_length=8, regex=r"^(?=.*\d)(?=.*[a-zA-Z])[a-zA-Z0-9]{7,}$"
    )


class Me200(BaseModel):
    """api/v1/account/me http200 response validation model"""
    username: constr(max_length=24, min_length=6, regex=r"^[a-zA-Z]+([_-]?[a-zA-Z0-9])*$")
    id: int
    rule_level: int
    activated: bool
    partner_id: int
    email: str

class RefreshData(BaseModel):
    """api/v1/account/refresh request validation model"""
    refreshToken: constr(min_length=6)


class Refresh401(BaseModel):
    """api/v1/account/refresh http401 response validation model"""
    title: str = "Нет такого пользователя или неверный токен"


class Login401(BaseModel):
    """api/v1/account/login http401 response validation model"""
    title: Literal[
        "Неверный логин или пароль",
        "Ожидайте активации вашего аккаунта администрацией ресурса",
    ]


class Refresh200(BaseModel):
    """api/v1/account/refresh http200 response validation model"""
    accessToken: str
    refreshToken: str
