"""
Server's run file
"""
import logging
import pathlib
from datetime import datetime

import uvicorn

from config import HOST, PORT
from src.custom_router import FalconRouter
from src.middleware import AuthMiddleware, CorsMiddleware
from src.utils import api

pathlib.Path("logs").mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename="logs/%s.txt" % datetime.today().strftime("%Y-%m-%d"),
    level=logging.INFO,
    format="[%(asctime)s:%(levelname)s] %(name)s - "
    "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
router = FalconRouter(
    "asgi",
    route_groups={
        "api": {
            "v1": {
                "account": {
                    "login": True,
                    "register": True,
                    "refresh": True,
                    # "me": True,
                },
                "product": {
                    "get_products": True,
                    # "get_products_by_user": True,
                    "update_offer": True,
                },
            }
        }
    },
    add_trailing_slash=True,
    middleware=[
        AuthMiddleware(),
        CorsMiddleware(),
    ],
    cors_enable=True,
    api=api,
)


if __name__ == "__main__":
    uvicorn.run(router.app, host=HOST, port=PORT, log_level="info")
