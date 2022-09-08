from pydantic import BaseModel, Field, constr
from spectree import Tag
from typing import Literal

Account_tag = Tag(name="Аккаунт", description="🧾🧾")


class register_200(BaseModel):
    status: bool
    title: str = "Напишите администратору сервиса для активации аккаунта"


class register_401(BaseModel):
    title: str = "Пользователь с таким логином уже существует"


class register_data(BaseModel):
    username: constr(max_length=24,
                     min_length=6,
                     regex=r"^[a-zA-Z]+([_-]?[a-zA-Z0-9])*$"
                     )
    password: constr(max_length=24,
                     min_length=8,
                     regex=r"^(?=.*\d)(?=.*[a-zA-Z])[a-zA-Z0-9]{7,}$"
                     )


class login_200(BaseModel):
    accessToken: str
    refreshToken: str


class login_data(BaseModel):
    username: constr(max_length=24,
                     min_length=6,
                     regex=r"^[a-zA-Z]+([_-]?[a-zA-Z0-9])*$"
                     )
    password: constr(max_length=24,
                     min_length=8,
                     regex=r"^(?=.*\d)(?=.*[a-zA-Z])[a-zA-Z0-9]{7,}$"
                     )


class me_data(BaseModel):
    username: constr(max_length=24,
                     min_length=6,
                     regex=r"^[a-zA-Z]+([_-]?[a-zA-Z0-9])*$"
                     )


class me_200(BaseModel):
    user: constr(max_length=24,
                 min_length=6,
                 regex=r"^[a-zA-Z]+([_-]?[a-zA-Z0-9])*$"
                 )


class refresh_data(BaseModel):
    refreshToken: constr(min_length=6)


class refresh_401(BaseModel):
    title: str = "Нет такого пользователя или неверный токен"


class login_401(BaseModel):
    title: Literal["Неверный логин или пароль", "Ожидайте активации вашего аккаунта администрацией ресурса"]


class refresh_200(BaseModel):
    accessToken: str
    refreshToken: str
