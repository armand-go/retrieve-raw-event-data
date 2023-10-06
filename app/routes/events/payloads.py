from typing import Optional, List, Dict

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


class EventWithSmartContract(BaseModel):
    eventId: int
    title: str
    startDatetime: datetime
    endDatetime: datetime
    address: str
    locationName: Optional[str]
    totalTicketsCount: int
    assetUrl: Optional[str]
    lineUp: Optional[List[str]]
    ticketCollections: List[Dict]

    @staticmethod
    def from_entity(
        event: entities.Event,
        smart_contracts: List[entities.SmartContract]
    ) -> "EventWithSmartContract":
        return EventWithSmartContract(
            eventId=event.event_id,
            title=event.title,
            startDatetime=event.start_datetime,
            endDatetime=event.end_datetime,
            address=event.address,
            locationName=event.location_name,
            totalTicketsCount=event.total_tickets_count,
            assetUrl=event.asset_url,
            lineUp=event.line_up,
            ticketCollections=[
                {
                    "collectionName": sc.collection_name,
                    "scAddress": sc.crowdsale,
                    "collectionAddress": sc.collection_address,
                    "pricePerToken": sc.price_per_token,
                    "maxMintPerUser": sc.max_mint_per_user,
                    "saleSize": sc.sale_size
                } for sc in smart_contracts
            ]
        )
