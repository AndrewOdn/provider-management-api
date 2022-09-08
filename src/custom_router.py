import importlib
from typing import Dict, List, Union

from falcon import App as WApp
from falcon.asgi import App as AApp


class FalconRouter:
    def __init__(
        self,
        app_type: str = "asgi",
        route_groups: Union[Dict, None, str] = None,
        add_trailing_slash: bool = False,
        api: bool = False,
        **kwargs,
    ):
        self.app = self._create_app(app_type, **kwargs)
        self.app.req_options.strip_url_path_trailing_slash = add_trailing_slash
        self._route_groups = route_groups
        self._add_routes()
        api.register(self.app)

    @staticmethod
    def parse_branch(routes: Dict) -> List[str]:
        not_check = [key for key in routes.keys()]
        result = []
        for key in not_check:
            value = routes[key]
            if type(value) is dict:
                for ckey in value.keys():
                    nkey = key + "." + ckey
                    not_check.append(nkey)
                    routes[nkey] = value[ckey]
            elif value == True:
                result.append(key)
            elif type(value) is list:
                result += [key + "." + ckey for ckey in value]
        return result

    @staticmethod
    def _create_app(app_type, **kwargs) -> Union[WApp, AApp]:
        app_type = app_type.lower()
        if app_type not in ["asgi", "wsgi"]:
            raise ValueError("Invalid application type specified!")
        return WApp(**kwargs) if app_type == "wsgi" else AApp(**kwargs)

    def _add_routes(self):
        if not self._route_groups:
            return
        if isinstance(self._route_groups, str):
            self._route_groups = [self._route_groups]
        routes = FalconRouter.parse_branch(self._route_groups)
        for route_group in routes:
            route_module = importlib.import_module(route_group)
            route = getattr(route_module, "route", None)
            if not route:
                continue
            routes = [(route_group.strip().replace(".", "/"), route)]
            for route, handler in routes:
                self.app.add_route(f"/{route.strip().strip('/')}", handler)
