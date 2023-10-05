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
