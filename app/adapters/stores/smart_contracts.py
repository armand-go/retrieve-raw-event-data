from sqlalchemy.sql.expression import select
from sqlalchemy.dialects.postgresql import insert

from app.domain.errors import ErrNotFound
from .transactions import Transactions
from app.domain import entities
from .models import smart_contracts


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

    async def get(self, event_id: str) -> entities.SmartContract:
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
            ).first()
        except Exception as e:
            raise e
        else:
            if not smart_contract:
                raise ErrNotFound("SmartContract")
            return smart_contract._data[0].to_entity()
        finally:
            tx.clear()
