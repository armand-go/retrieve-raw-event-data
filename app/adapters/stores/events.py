from .transactions import Transactions
from sqlalchemy.sql.expression import select
from sqlalchemy.dialects.postgresql import insert

from typing import Optional

from app.domain import entities
from app.domain.errors import ErrNotFound
from .models import events


class Events:
    def __init__(self, transactions: Transactions) -> None:
        self.__transactions = transactions

    def event_to_db(self, event: entities.Event, exclude: Optional[dict] = None) -> dict:
        if not exclude:
            return event.model_dump()
        else:
            event_data = event.model_dump(exclude=exclude)

            new_event_data = {}
            for key in event_data.keys():
                new_event_data[key.lower()] = event_data[key]

            return new_event_data

    async def upsert(self, event: entities.Event, transaction: Transactions | None = None) -> None:
        tx = transaction or self.__transactions.start()

        query = (
            insert(events.Events)
            .values(self.event_to_db(event))
            .on_conflict_do_update(
                index_elements=[events.Events.eventId],
                set_=self.event_to_db(event, exclude={
                    "eventId",
                    "startDatetime",
                    "endDatetime",
                    "maxTicketPerUser",
                    "totalTicketsCount",
                    "address"
                }),
            )
        )

        try:
            tx.instance().execute(query)
        except Exception as e:
            tx.rollback()
            raise e

        if not transaction:
            tx.commit()

    async def get(self, event_id: str) -> entities.Event:
        tx = self.__transactions.start()

        try:
            event = (
                tx.instance().execute(
                    select(
                        events.Events
                    ).where(
                        events.Events.eventId == event_id
                    )
                )
            ).first()
        except Exception as e:
            raise e
        else:
            if not event:
                raise ErrNotFound("Event")
            return event._data[0].to_entity()
        finally:
            tx.clear()
