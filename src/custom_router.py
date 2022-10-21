from fastapi import FastAPI



class CustomRouter:
    def __init__(
            self,
            *args,
            **kwargs,
    ) -> object:
        self.title = kwargs['title']  # access args index like array does
        self.version = kwargs['version']
        self.description = kwargs['description']
        self.app = FastAPI(title=self.title, version=self.version, description=self.description)
        self._route_groups = args
        self._add_routes()

    def _add_routes(self):
        for route_group in self._route_groups:
            self.app.include_router(route_group)
