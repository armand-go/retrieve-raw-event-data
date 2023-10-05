from fastapi import APIRouter


class API:
    serve = APIRouter()

    def __init__(self, *args):
        for route in args:
            self.serve.include_router(route.ep)
