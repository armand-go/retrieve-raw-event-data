from typing import Any, Dict, List
from asyncio import TaskGroup
import re

from app.domain import entities
from app.domain.errors import ErrNotFound, ErrUnexpected
from app.adapters import stores


class Events:
    def __init__(self, store: stores.Events, smartContractStore: stores.SmartContracts):
        self.__store = store
        self.__smartContractStore = smartContractStore

    async def retrieve_single_event(self, event_id: str) -> entities.Event:
        try:
            event = await self.__store.get(event_id)
        except ErrNotFound as e:
            raise e
        except Exception:
            raise ErrUnexpected()
        else:
            return event

    async def update_event(self, event_id: str, new_data: Dict[str, Any]):
        try:
            event = await self.__store.get(event_id)
        except ErrNotFound as e:
            raise e
        except Exception:
            raise ErrUnexpected()

        for key, val in new_data.items():
            key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
            setattr(event, key, val)

        try:
            await self.__store.upsert(event)
        except Exception:
            raise ErrUnexpected()
        else:
            return event

    async def retrieve_event_with_ticket_collection(self, event_id: str) -> entities.Event:
        try:
            async with TaskGroup() as tg:
                futureEvent = tg.create_task(self.__store.get(event_id))
                futureSmartContracts = tg.create_task(
                    self.__smartContractStore.get_by_event_id(event_id)
                )

            event = futureEvent.result()
            smart_contracts = futureSmartContracts.result()
        except* ErrNotFound as e:
            raise e
        except* Exception:
            raise ErrUnexpected()
        else:
            return event, smart_contracts

    async def list_events(self, filters: List[dict]) -> List[entities.Event]:
        try:
            event_list = await self.__store.list(filters)
        except Exception:
            raise ErrUnexpected()
        else:
            return event_list
