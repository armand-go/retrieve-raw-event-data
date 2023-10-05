from fastapi import APIRouter

from app.domain import usecases
from . import payloads


class Events:
    ep = APIRouter(prefix="/events")
    __eventsUC: usecases.Events

    def __init__(self, eventsUsecases: usecases.Events):
        Events.__eventsUC = eventsUsecases

    @staticmethod
    @ep.get("/{id}", response_model=payloads.Event)
    async def retrieve_single_event(id: str):
        event = await Events.__eventsUC.retrieve_single_event(id)
        return event
