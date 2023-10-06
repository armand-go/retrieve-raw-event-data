from sqlalchemy.sql.expression import select
from sqlalchemy.dialects.postgresql import insert

from typing import List

from .transactions import Transactions
from .models import smart_contracts
from app.domain import entities


class SmartContracts:
    def __init__(self, transactions: Transactions) -> None:
        self.__transactions = transactions

    async def insert(
        self,
        smart_contract: entities.SmartContract,
        transaction: Transactions | None = None
    ) -> None:
        tx = transaction or self.__transactions.start()

        query = (
            insert(smart_contracts.SmartContract)
            .values(smart_contract.model_dump())
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
