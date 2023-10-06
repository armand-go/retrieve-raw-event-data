from sqlalchemy.sql.expression import select
from sqlalchemy.dialects.postgresql import insert

from typing import List

from app.domain.errors import ErrNotFound
from .transactions import Transactions
from .models import smart_contracts
from app.domain import entities


class SmartContracts:
    def __init__(self, transactions: Transactions) -> None:
        self.__transactions = transactions

    async def upsert(
        self,
        smart_contract: entities.SmartContract,
        transaction: Transactions | None = None
    ) -> None:
        tx = transaction or self.__transactions.start()

        query = (
            insert(smart_contracts.SmartContract)
            .values(smart_contract.model_dump())
            .on_conflict_do_update(index_elements=[
                smart_contracts.SmartContract.crowdsale
            ], set_=smart_contract.model_dump(include={"collection_name"})
            )
        )

        try:
            tx.instance().execute(query)
        except Exception as e:
            tx.rollback()
            raise e

        if not transaction:
            tx.commit()

    async def get_by_event_id(self, event_id: str) -> List[entities.SmartContract]:
        tx = self.__transactions.start()

        try:
            smart_contract = (
                tx.instance().execute(
                    select(
                        smart_contracts.SmartContract
                    ).where(
                        smart_contracts.SmartContract.event_id == event_id
                    )
                )
            ).scalars()
        except Exception as e:
            raise e
        else:
            return [sm.to_entity() for sm in smart_contract]
        finally:
            tx.clear()

    async def get(self, smart_contract_address: str) -> entities.SmartContract:
        tx = self.__transactions.start()

        try:
            sc = (
                tx.instance().execute(
                    select(
                        smart_contracts.SmartContract
                    ).where(
                        smart_contracts.SmartContract.crowdsale == smart_contract_address
                    )
                )
            ).first()
        except Exception as e:
            raise e
        else:
            if not sc:
                raise ErrNotFound("SmartContract")
            return sc._data[0].to_entity()
        finally:
            tx.clear()