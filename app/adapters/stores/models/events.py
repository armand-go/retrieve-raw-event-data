from . import Base

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import ARRAY

from app.domain import entities

_SCHEMA = "data"


class Events(Base):
    __tablename__ = "events"
    __table_args__ = {"schema": _SCHEMA}

    eventId = Column(Integer, primary_key=True, name="eventid")
    title = Column(String, nullable=False)
    startDatetime = Column(DateTime, nullable=False, name="startdatetime")
    endDatetime = Column(DateTime, nullable=False, name="enddatetime")
    locationName = Column(String, name="locationname")
    address = Column(String, nullable=False)
    totalTicketsCount = Column(Integer, nullable=False, name="totalticketscount")
    maxTicketPerUser = Column(Integer, nullable=False, name="maxticketperuser")
    saleStartDate = Column(DateTime, nullable=False, name="salestartdate")
    lineUp = Column(ARRAY(String), name="lineup")
    assetUrl = Column(String, name="asseturl")

    def to_entity(self) -> entities.Event:
        return entities.Event(
            eventId=self.eventId,
            title=self.title,
            startDatetime=self.startDatetime,
            endDatetime=self.endDatetime,
            locationName=self.locationName,
            address=self.address,
            totalTicketsCount=self.totalTicketsCount,
            maxTicketPerUser=self.maxTicketPerUser,
            saleStartDate=self.saleStartDate,
            lineUp=self.lineUp,
            assetUrl=self.assetUrl
        )
