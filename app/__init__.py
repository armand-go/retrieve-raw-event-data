from fastapi import FastAPI
from .dependencies import BillyAPI

serve = FastAPI(title="TechnicalTestBilly", version="1")


@serve.get("/")
def ping():
    return "."


billy_routes = BillyAPI().router.serve
serve.include_router(billy_routes)
