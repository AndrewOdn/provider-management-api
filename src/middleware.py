from falcon import Response, Request
from api.v1.account.login import Login
from api.v1.account.refresh import Refresh
from api.v1.account.register import Register
from spectree.plugins.falcon_plugin import DocPageAsgi, OpenAPIAsgi
import logging
import falcon

from .utils import token_is_valid
from config import ACCESS_SECRET, TOKEN_NAME


class AuthMiddleware:
    async def process_startup(self, scope, event):
        pass

    async def process_shutdown(self, scope, event):
        pass

    async def process_request(self, req, resp):
        pass

    async def process_resource(self, req: Request, res: Response, resource, params):
        logging.debug("Processing request in AuthMiddleware: ")
        if (
            isinstance(resource, Login)
            or isinstance(resource, Register)
            or isinstance(resource, Refresh)
            or isinstance(resource, DocPageAsgi)
            or isinstance(resource, OpenAPIAsgi)
        ):
            logging.debug("Login or Register, dont't need token")
            return
        token = req.get_header(TOKEN_NAME, required=True)
        if not token:
            raise falcon.HTTPUnauthorized(
                "Auth token required",
                "Please provide an auth token as part of the request.",
            )
        token_data = await token_is_valid(token, ACCESS_SECRET)
        if not token_data:
            raise falcon.HTTPUnauthorized(
                "Authentication required", "Token not valid or expired"
            )
        req.context = token_data

    async def process_response(
        self, req: Request, res: Response, resource, req_succeeded
    ):
        pass

    async def process_request_ws(self, req, ws):
        pass

    async def process_resource_ws(self, req, ws, resource, params):
        pass


whitelisted_origins = [
    "http://localhost:8081",
    "http://localhost:3000",
]
whitelisted_methods = ["GET", "POST", "OPTIONS", "DELETE"]


class CorsMiddleware:
    async def process_request(self, req, resp):
        if req.method == "OPTIONS":
            success = False
            # validate request origin
            if "ORIGIN" in req.headers:
                # validate request origin
                if req.headers["ORIGIN"] in whitelisted_origins:
                    # validate request method
                    if req.method in whitelisted_methods:
                        success = True
                    else:
                        # you can put required resp.status and resp.media here
                        pass
                else:
                    # you can put required resp.status and resp.media here
                    pass
            else:
                # you can put required resp.status and resp.media here
                pass
            if success:
                resp.set_header("Access-Control-Allow-Origin", req.headers["ORIGIN"])
            else:
                # exit request
                resp.complete = True

    async def process_response(self, req, resp, resource, req_succeeded):
        if (
            req_succeeded
            and "ORIGIN" in req.headers
            and req.method == "OPTIONS"
            and req.get_header("Access-Control-Request-Method")
        ):
            # NOTE: This is a CORS preflight request. Patch the response accordingly.

            allow = resp.get_header("Allow")
            resp.delete_header("Allow")

            allow_headers = req.get_header(
                "Access-Control-Request-Headers", default="*"
            )

            resp.set_headers(
                (
                    ("Access-Control-Allow-Methods", allow),
                    ("Access-Control-Allow-Headers", allow_headers),
                    ("Access-Control-Max-Age", "86400"),  # 24 hours
                )
            )