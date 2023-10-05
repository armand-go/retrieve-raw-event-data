from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel):
    eventId: int
    title: str
    startDatetime: datetime
    endDatetime: datetime
    locationName: Optional[str]
    address: str
    totalTicketsCount: int
    maxTicketPerUser: int
    saleStartDate: datetime
    lineUp: Optional[List[str]]
    assetUrl: Optional[str]

    class Filters(BaseModel):
        title: Optional[str] = None
        startDatetime: Optional[str] = None
        endDatetime: Optional[str] = None
        saleStartDate: Optional[str] = None
        operator: Optional[str] = None

        def to_filters(self) -> List[dict]:
            res: List[dict] = []
            if self.title:
                res.append({"field": "title", "operator": "==", "value": self.title})

            operator = self.operator or ">="
            if self.startDatetime:
                res.append(
                    {"field": "startDatetime", "operator": operator, "value": self.startDatetime}
                )

            if self.endDatetime:
                res.append(
                    {"field": "endDatetime", "operator": operator, "value": self.endDatetime}
                )

            if self.saleStartDate:
                res.append(
                    {"field": "saleStartDate", "operator": operator, "value": self.saleStartDate}
                )

            return res
