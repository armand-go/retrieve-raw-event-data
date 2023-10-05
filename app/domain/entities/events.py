from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel):
    event_id: int
    title: str
    start_datetime: datetime
    end_datetime: datetime
    location_name: Optional[str]
    address: str
    total_tickets_count: int
    max_ticket_per_user: int
    sale_start_date: datetime
    line_up: Optional[List[str]]
    asset_url: Optional[str]
