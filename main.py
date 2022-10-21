import uvicorn
from src.custom_router import CustomRouter
from api.v1.account import login, register, refresh, me
from api.v1.product import get_products, update_offer
from api.v1.product.favorite import set, remove
from config import HOST, PORT
CRoute = CustomRouter(
    login.router,
    register.router,
    refresh.router,
    me.router,
    get_products.router,
    update_offer.router,
    set.router,
    remove.router,
    title="provider-management-api",
    version="1.0.1",
    description="Апи для взаимодействия Front'a и сервера bk",
)


if __name__ == "__main__":
    uvicorn.run(CRoute.app, host=HOST, port=PORT, log_level="info")