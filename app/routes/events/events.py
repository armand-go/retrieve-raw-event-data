from fastapi import APIRouter, Depends
from typing import List

from app.domain import usecases
from . import payloads


class Events:
    ep = APIRouter(prefix="/events")
    __eventsUC: usecases.Events

    def __init__(self, eventsUsecases: usecases.Events):
        Events.__eventsUC = eventsUsecases

    @staticmethod
    @ep.get("/list", response_model=List[payloads.Event])
    async def list_events(filter: payloads.Event.Filters = Depends(payloads.Event.Filters)):
        event_list = await Events.__eventsUC.list_events(filter.to_filters())
        return [payloads.Event.from_entity(event) for event in event_list]

    @staticmethod
    @ep.get("/withTicketsCollection/{id}", response_model=payloads.EventWithSmartContract)
    async def retrieve_event_with_ticket_collection(id: str):
        event, smart_contracts = await Events.__eventsUC.retrieve_event_with_ticket_collection(id)
        return payloads.EventWithSmartContract.from_entity(event, smart_contracts)

    @staticmethod
    @ep.get("/{id}", response_model=payloads.Event)
    async def retrieve_single_event(id: str):
        event = await Events.__eventsUC.retrieve_single_event(id)
        return payloads.Event.from_entity(event)
