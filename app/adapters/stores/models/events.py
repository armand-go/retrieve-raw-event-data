from . import Base

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import ARRAY

from app.domain import entities

_SCHEMA = "data"


class Events(Base):
    __tablename__ = "events"
    __table_args__ = {"schema": _SCHEMA}

    event_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    location_name = Column(String)
    address = Column(String, nullable=False)
    total_tickets_count = Column(Integer, nullable=False)
    max_ticket_per_user = Column(Integer, nullable=False)
    sale_start_date = Column(DateTime, nullable=False)
    line_up = Column(ARRAY(String))
    asset_url = Column(String)

    def to_entity(self) -> entities.Event:
        return entities.Event(
            event_id=self.event_id,
            title=self.title,
            start_datetime=self.start_datetime,
            end_datetime=self.end_datetime,
            location_name=self.location_name,
            address=self.address,
            total_tickets_count=self.total_tickets_count,
            max_ticket_per_user=self.max_ticket_per_user,
            sale_start_date=self.sale_start_date,
            line_up=self.line_up,
            asset_url=self.asset_url
        )
