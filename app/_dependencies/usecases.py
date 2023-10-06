from .core import Core
from .store import Store

from app.domain import usecases


class Usecases:
    core: Core
    store: Store

    events: usecases.Events

    def __init__(self, store: Store) -> None:
        self.store = store

        self.events = usecases.Events(
            store=self.store.events,
            smartContractStore=self.store.smart_contracts
        )
        self.smart_contracts = usecases.SmartContracts(
            store=self.store.smart_contracts
        )
