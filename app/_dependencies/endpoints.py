from .usecases import Usecases

from app.routes import (
    events as events_ep,
    smart_contracts as smart_contracts_ep
)


class Endpoints:
    usecases: Usecases

    def __init__(self, usecases: Usecases) -> None:
        self.usecases = usecases

        self.events = events_ep.Events(self.usecases.events)
        self.smart_contracts = smart_contracts_ep.SmartContracts(self.usecases.smart_contracts)
