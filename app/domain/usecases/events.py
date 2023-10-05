from typing import List

from app.domain import entities
from app.domain.errors import ErrNotFound, ErrUnexpected
from app.adapters import stores


class Events:
    def __init__(self, store: stores.Events):
        self.__store = store

    async def retrieve_single_event(self, event_id: str) -> entities.Event:
        try:
            event = await self.__store.get(event_id)
        except ErrNotFound as e:
            raise e
        except Exception:
            raise ErrUnexpected()
        else:
            return event

    async def list_events(self, filters: List[dict]) -> List[entities.Event]:
        try:
            event_list = await self.__store.list(filters)
        except Exception:
            raise ErrUnexpected()
        else:
            return event_list
