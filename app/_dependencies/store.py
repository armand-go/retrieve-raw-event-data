from .core import Core

from app.adapters import stores


class Store:
    core: Core
    transactions: stores.Transactions

    events: stores.Events

    def __init__(self, core: Core) -> None:
        self.core = core
        self.transactions = stores.Transactions(engine=self.core.postgres)

        self.events = stores.Events(transactions=self.transactions)
