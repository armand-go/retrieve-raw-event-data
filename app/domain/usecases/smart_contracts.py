import re
from typing import Any, Dict

from app.domain import entities
from app.domain.errors import ErrNotFound, ErrUnexpected
from app.adapters import stores


class SmartContracts:
    def __init__(self, store: stores.SmartContracts):
        self.__store = store

    async def retrieve_single_sc(self, smart_contract_address: str) -> entities.Event:
        try:
            sc = await self.__store.get(smart_contract_address)
        except ErrNotFound as e:
            raise e
        except Exception:
            raise ErrUnexpected()
        else:
            return sc

    async def update_sc(self, smart_contract_address: str, new_data: Dict[str, Any]):
        try:
            sc = await self.__store.get(smart_contract_address)
        except ErrNotFound as e:
            raise e
        except Exception:
            raise ErrUnexpected()

        for key, val in new_data.items():
            key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
            setattr(sc, key, val)

        try:
            await self.__store.upsert(sc)
        except Exception:
            raise ErrUnexpected()
        else:
            return sc

