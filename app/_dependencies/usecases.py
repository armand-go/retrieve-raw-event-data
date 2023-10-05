from .core import Core
from .store import Store

from app.domain import usecases


class Usecases:
    core: Core
    store: Store

    events: usecases.Events

    def __init__(self, core: Core, store: Store) -> None:
        self.core = core
        self.store = store

        self.events = usecases.Events(store=self.store.events)
