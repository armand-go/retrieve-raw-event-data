from sqlalchemy import Column
from sqlalchemy.sql.expression import select
from sqlalchemy.dialects.postgresql import insert

from typing import Any, Iterable, List

from app.domain.errors import ErrNotFound
from .transactions import Transactions
from app.domain import entities
from .models import events


def add_filters_to_query(query, field: Column, filt: dict):
    value: Any
    match str(filt["operator"]).upper():
        case "IN":
            value = filt["value"].split(",")
            query = query.where(field.in_(value))
        case "!=":
            query = query.where(field != filt["value"])
        case ">=":
            query = query.where(field >= filt["value"])
        case ">":
            query = query.where(field > filt["value"])
        case "<=":
            query = query.where(field <= filt["value"])
        case "<":
            query = query.where(field <= filt["value"])
        case _:
            query = query.where(field == filt["value"])
    return query


class Events:
    filter_by = {
        "title": events.Events.title,
        "startDatetime": events.Events.start_datetime,
        "endDatetime": events.Events.end_datetime,
        "saleStartDate": events.Events.sale_start_date,
    }

    def __init__(self, transactions: Transactions) -> None:
        self.__transactions = transactions

    async def upsert(self, event: entities.Event, transaction: Transactions | None = None) -> None:
        tx = transaction or self.__transactions.start()

        query = (
            insert(events.Events)
            .values(event.model_dump())
            .on_conflict_do_update(
                index_elements=[events.Events.event_id],
                set_=event.model_dump(exclude={
                    "event_id",
                    "start_datetime",
                    "end_datetime",
                    "max_ticket_per_user",
                    "total_tickets_count",
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
                        events.Events.event_id == event_id
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

    async def list(self, filters: Iterable[dict] | None = None,) -> List[entities.Event]:
        query = select(events.Events)

        filters = filters or []

        for filt in filters:
            field = self.filter_by.get(filt["field"])
            if not field:
                continue
            query = add_filters_to_query(query, field, filt)

        tx = self.__transactions.start()

        try:
            events_list = tx.instance().execute(query).scalars()
        except Exception as e:
            raise e
        else:
            if not events:
                return []

            return [event.to_entity() for event in events_list]
        finally:
            tx.clear()
