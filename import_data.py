import asyncio

from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Tuple
from dotenv import dotenv_values
from datetime import datetime
from asyncio import TaskGroup
import pandas as pd
import json

from app.adapters.stores import Events, SmartContracts, Transactions
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
    def dict_entry(
        entry: Dict,
        index: int,
        required: List[str],
        conditions: Dict[
            str, List[Callable[[Any, str, int], Optional[Details]]]
        ],
    ) -> List[Details]:
        details: List[Details] = []

        for field in required:
            fields = None
            if "." in field:
                fields = field.split(".")
            if fields:
                key = f"entry.{index}"
                data = entry

                for field in fields:
                    key += f".{field}"

                    if field not in data:
                        details.append(
                            Details(
                                key=key,
                                message="required"
                            )
                        )
                        break
                    else:
                        data = data.get(field)

            elif field not in entry:
                details.append(
                    Details(
                        key=f"entry.{index}.{field}",
                        message="required"
                    )
                )

            if details:
                return details

        for field, validators in conditions.items():
            fields = None
            if "." in field:
                fields = field.split(".")

            if fields:
                data = entry
                for field in fields:
                    data = data.get(field)
                data = Input.clean(str(data))
            else:
                data = Input.clean(str(entry.get(field)))

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

    @staticmethod
    def is_bool(data: Any, field_name: str, idx: int) -> Optional[Details]:
        if isinstance(data, bool):
            return None
        if str(data).lower() in ("true", "false", "t", "f", "0", "1"):
            return None
        return Details(key=f"rows.{idx}.{field_name}", message="not_boolean", value=data)


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
    def cell_to_dict(
        data, default: None | Dict = None
    ) -> Dict | None:
        if data is None:
            return default

        data = Input.clean(data)

        return json.loads(data)

    @staticmethod
    def cell_to_bool(data) -> bool:
        return Input.clean(str(data)).lower() == "true"

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
        self.smartContractStore = SmartContracts(transactions=self.transactions)

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
                        event_id=Input.cell_to_int(row["id"]),
                        title=Input.clean(row["event title"]),
                        start_datetime=Input.cell_to_datetime(row["event start date"]),
                        end_datetime=Input.cell_to_datetime(row["event end date"]),
                        location_name=Input.clean(location) if location else None,
                        address=Input.clean(row["address of the location"]),
                        total_tickets_count=Input.cell_to_int(row["total ticket number"]),
                        max_ticket_per_user=Input.cell_to_int(row["maximum tickets per user"]),
                        sale_start_date=Input.cell_to_datetime(row["sale start date"], "%d/%m/%Y"),
                        line_up=line_up or None,
                        asset_url=Input.clean(
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

    async def import_smart_contract(self) -> None:
        async def __parse_smart_contracts() -> AsyncGenerator[
            Tuple[entities.Event, None] | Tuple[None, List[Details]], None
        ]:
            for index, dat in enumerate(data):
                detail = Validate.dict_entry(
                    dat,
                    index,
                    [
                        "event_id",
                        "collection_name",
                        "smart_contract.crowdsale",
                        "smart_contract.collection",
                        "smart_contract.multisig",
                        "smart_contract.sale_params.is_presale",
                        "smart_contract.sale_params.metadata_list",
                        "smart_contract.sale_params.price_per_token",
                        "smart_contract.sale_params.max_mint_per_user",
                        "smart_contract.sale_params.sale_size",
                        "smart_contract.sale_params.sale_currency",
                        "smart_contract.sale_params.start_time",
                        "smart_contract.sale_params.end_time"
                    ],
                    {
                        "event_id": [Validate.not_empty, Validate.is_int],
                        "collection_name": [Validate.not_empty],
                        "smart_contract.crowdsale": [Validate.not_empty],
                        "smart_contract.collection": [Validate.not_empty],
                        "smart_contract.multisig": [Validate.not_empty],
                        "smart_contract.sale_params.is_presale": [
                            Validate.not_empty, Validate.is_bool
                        ],
                        "smart_contract.sale_params.metadata_list": [Validate.not_empty],
                        "smart_contract.sale_params.price_per_token": [
                            Validate.not_empty, Validate.is_int
                        ],
                        "smart_contract.sale_params.max_mint_per_user": [
                            Validate.not_empty, Validate.is_int
                        ],
                        "smart_contract.sale_params.sale_size": [
                            Validate.not_empty, Validate.is_int
                        ],
                        "smart_contract.sale_params.sale_currency": [Validate.not_empty],
                        "smart_contract.sale_params.start_time": [
                            Validate.not_empty, Validate.is_int
                        ],
                        "smart_contract.sale_params.end_time": [
                            Validate.not_empty, Validate.is_int
                        ],
                    },
                )

                if detail:
                    yield None, detail
                else:
                    yield entities.SmartContract(
                        event_id=Input.cell_to_int(dat["event_id"]),
                        collection_name=Input.clean(dat["collection_name"]),
                        crowdsale=Input.clean(dat["smart_contract"]["crowdsale"]),
                        collection_address=Input.clean(dat["smart_contract"]["collection"]),
                        multisig=Input.clean(dat["smart_contract"]["multisig"]),
                        is_presale=dat["smart_contract"]["sale_params"]["is_presale"],
                        metadata_list=dat["smart_contract"]["sale_params"]["metadata_list"],
                        price_per_token=Input.cell_to_int(
                            dat["smart_contract"]["sale_params"]["price_per_token"]
                        ),
                        max_mint_per_user=Input.cell_to_int(
                            dat["smart_contract"]["sale_params"]["max_mint_per_user"]
                        ),
                        sale_size=Input.cell_to_int(
                            dat["smart_contract"]["sale_params"]["sale_size"]
                        ),
                        sale_currency=dat["smart_contract"]["sale_params"]["sale_currency"],
                        start_time=Input.cell_to_int(
                            dat["smart_contract"]["sale_params"]["start_time"]
                        ),
                        end_time=Input.cell_to_int(
                            dat["smart_contract"]["sale_params"]["end_time"]
                        ),
                    ), None

        details: List[Details] = []
        with open("smart-contracts-data.json") as json_file:
            data = json.load(json_file)

        tx = self.transactions.start()

        try:
            async with TaskGroup() as tg:
                async for smart_contract, detail in __parse_smart_contracts():
                    if detail:
                        details += detail
                    elif smart_contract:
                        tg.create_task(self.smartContractStore.insert(smart_contract, tx))
        except Exception as e:
            tx.rollback()
            raise e

        if details:
            print(ErrInvalidData("file", "corrupted_file", details).to_json())
            # raise ErrInvalidData("file", "corrupted_file", details)

        try:
            tx.commit()
        except Exception as e:
            tx.rollback()
            raise e


if __name__ == "__main__":
    _import = Import()
    asyncio.run(_import.import_events())
    asyncio.run(_import.import_smart_contract())
