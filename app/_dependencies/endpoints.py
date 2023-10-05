from .usecases import Usecases

from app.routes import events as events_ep


class Endpoints:
    usecases: Usecases

    def __init__(self, usecases: Usecases) -> None:
        self.usecases = usecases

        self.events = events_ep.Events(self.usecases.events)
