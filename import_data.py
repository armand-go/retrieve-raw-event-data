import asyncio

from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Tuple
from dotenv import dotenv_values
from datetime import datetime
from asyncio import TaskGroup
import pandas as pd

from app.adapters.stores import Transactions, Events
from app.domain.errors import Details, ErrInvalidData
from pandas.core.series import Series
from app._dependencies import Core
from app.domain import entities

from rfc3986 import urlparse


class Validate:
    @staticmethod
    def row(
        index: int,
        row: Series,
        required: List[str],
        conditions: Dict[
            str, List[Callable[[Any, str, int], Optional[Details]]]
        ],
    ) -> List[Details]:
        details: List[Details] = []

        for field in required:
            if field not in row:
                details.append(
                    Details(
                        key=f"rows.{index}.{field}",
                        message="required"
                    )
                )

            if details:
                return details

        for field, validators in conditions.items():
            data = Input.clean(str(row.get(field)))
            for validator in validators:
                res = validator(data, field, index)
                if res:
                    details.append(res)
        return details

    @staticmethod
    def not_empty(data: Any, field_name: str, idx: int) -> Optional[Details]:
        if not data:
            return Details(
                key=f"rows.{idx}.{field_name}",
                message="empty",
                value={"actual": data, "expected": "Non empty data"},
            )

        return None

    @staticmethod
    def is_datetime(format: str = "%d/%m/%Y %H:%M"):
        def __matcher(data: Any, field_name: str, idx: int) -> Optional[Details]:
            if data:
                try:
                    datetime.strptime(data, format)
                except (TypeError, ValueError):
                    return Details(
                        key=f"rows.{idx}.{field_name}",
                        message="expect_datetime",
                        value={"actual": data, "expected_format": format},
                    )

            return None
        return __matcher

    @staticmethod
    def is_int(data: Any, field_name: str, idx: int) -> Optional[Details]:
        if data:
            try:
                int(data)
            except ValueError as e:
                print(e)
                return Details(key=f"rows.{idx}.{field_name}", message="not_integer", value=data)

        return None

    @staticmethod
    def is_url(data: Any, field_name: str, idx: int) -> Optional[Details]:
        if data:
            try:
                res = urlparse(data)
            except ValueError:
                return Details(key=f"rows.{idx}.{field_name}", message="not_url", value=data)
            else:
                if not res.hostname and not res.path:
                    return Details(key=f"rows.{idx}.{field_name}", message="not_url", value=data)

        return None


class Input:
    @staticmethod
    def clean(data: str) -> str | None:
        if data:
            return data.strip().rstrip("\r\n")
        return None

    @staticmethod
    def safe_cast(val: str, to_type, default=None):
        try:
            if val:
                return to_type(Input.clean(val))
            else:
                return default
        except (ValueError, TypeError):
            return default
        except Exception as e:
            raise e

    @staticmethod
    def cell_to_list(data: str, sep: str = ";", default: None | List = None) -> List[str] | None:
        if data is None:
            return default
        return [Input.clean(txt) for txt in data.split(sep)]  # type: ignore[misc]

    @staticmethod
    def cell_to_datetime(date: str, format: str = "%d/%m/%Y %H:%M") -> datetime | None:
        date = Input.clean(date)
        if date:
            return datetime.strptime(date, format)
        return None

    @staticmethod
    def cell_to_int(data: Any, default: int = 0) -> int:
        return Input.safe_cast(str(data), int, default)


class Import:
    def __init__(self) -> None:
        self.config = dotenv_values(".env")
        core = Core(config=self.config)

        self.transactions = Transactions(engine=core.postgres)
        self.eventStore = Events(transactions=self.transactions)

    async def import_events(self) -> None:
        async def __parse_events() -> AsyncGenerator[
            Tuple[entities.Event, None] | Tuple[None, List[Details]], None
        ]:
            for index, row in df.iterrows():
                detail = Validate.row(
                    index,
                    row,
                    [
                        "id",
                        "event title",
                        "event start date",
                        "event end date",
                        "address of the location",
                        "total ticket number",
                        "maximum tickets per user",
                        "sale start date",
                        "event image or video url (mp4 or png or jpeg)",
                    ],
                    {
                        "id": [Validate.not_empty],
                        "event title": [Validate.not_empty],
                        "event start date": [Validate.not_empty, Validate.is_datetime()],
                        "event end date": [Validate.not_empty, Validate.is_datetime()],
                        "address of the location": [Validate.not_empty],
                        "total ticket number": [Validate.not_empty, Validate.is_int],
                        "maximum tickets per user": [Validate.not_empty, Validate.is_int],
                        "sale start date": [Validate.not_empty, Validate.is_datetime("%d/%m/%Y")],
                        "event image or video url (mp4 or png or jpeg)": [
                            Validate.not_empty, Validate.is_url
                        ]
                    },
                )

                if detail:
                    yield None, detail
                else:
                    line_up = None
                    if row["line up (optional)"]:
                        line_up = Input.clean(str(row["line up (optional)"])).split("-")

                    location = row["name of the location hosting the event (optional)"]
                    url_extension = Input.clean(
                        row["event image or video url (mp4 or png or jpeg)"]
                    ).split(".")[-1]

                    yield entities.Event(
                        eventId=Input.cell_to_int(row["id"]),
                        title=Input.clean(row["event title"]),
                        startDatetime=Input.cell_to_datetime(row["event start date"]),
                        endDatetime=Input.cell_to_datetime(row["event end date"]),
                        locationName=Input.clean(location) if location else None,
                        address=Input.clean(row["address of the location"]),
                        totalTicketsCount=Input.cell_to_int(row["total ticket number"]),
                        maxTicketPerUser=Input.cell_to_int(row["maximum tickets per user"]),
                        saleStartDate=Input.cell_to_datetime(row["sale start date"], "%d/%m/%Y"),
                        lineUp=line_up or None,
                        assetUrl=Input.clean(
                            row["event image or video url (mp4 or png or jpeg)"]
                        ) if url_extension in ["mp4", "png", "jpeg"] else None
                    ), None

        details: List[Details] = []
        df = pd.read_csv("./organizers-data.csv")
        df = df.fillna("")

        tx = self.transactions.start()

        try:
            async with TaskGroup() as tg:
                async for event, detail in __parse_events():
                    if detail:
                        details += detail
                    elif event:
                        tg.create_task(self.eventStore.upsert(event, tx))
        except Exception as e:
            tx.rollback()
            raise e

        if details:
            raise ErrInvalidData("file", "corrupted_file", details)

        try:
            tx.commit()
        except Exception as e:
            tx.rollback()
            raise e


if __name__ == "__main__":
    _import = Import()
    asyncio.run(_import.import_events())
