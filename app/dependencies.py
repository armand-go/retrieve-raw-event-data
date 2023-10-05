from dotenv import dotenv_values

from ._dependencies import Core, Endpoints, Store, Usecases
from .api import API


class BillyAPI:
    config = dotenv_values(".env")

    core = Core(config=config)
    store = Store(core=core)
    usecases = Usecases(core=core, store=store)

    endpoints = Endpoints(usecases=usecases)

    router = API(
        endpoints.events
    )
