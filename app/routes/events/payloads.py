from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

from app.domain import entities


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

    @staticmethod
    def from_entity(event: entities.Event) -> "Event":
        return Event(
            eventId=event.event_id,
            title=event.title,
            startDatetime=event.start_datetime,
            endDatetime=event.end_datetime,
            locationName=event.location_name,
            address=event.address,
            totalTicketsCount=event.total_tickets_count,
            maxTicketPerUser=event.max_ticket_per_user,
            saleStartDate=event.sale_start_date,
            lineUp=event.line_up,
            assetUrl=event.asset_url
        )