from typing import Optional, List

from pydantic import BaseModel

from app.domain import entities


class SmartContract(BaseModel):
    eventId: int
    collectionName: str
    crowdsale: str
    collectionAddress: str
    multisig: str
    isPresale: bool
    metadataList: List[str]
    pricePerToken: int
    maxMintPerUser: int
    saleSize: int
    saleCurrency: dict
    startTime: int
    endTime: int

    class Update(BaseModel):
        collectionName: Optional[str]

    @staticmethod
    def from_entity(sc: entities.SmartContract) -> "SmartContract":
        return SmartContract(
            eventId=sc.event_id,
            collectionName=sc.collection_name,
            crowdsale=sc.crowdsale,
            collectionAddress=sc.collection_address,
            multisig=sc.multisig,
            isPresale=sc.is_presale,
            metadataList=sc.metadata_list,
            pricePerToken=sc.price_per_token,
            maxMintPerUser=sc.max_mint_per_user,
            saleSize=sc.sale_size,
            saleCurrency=sc.sale_currency,
            startTime=sc.start_time,
            endTime=sc.end_time
        )
