from . import Base

from sqlalchemy import Boolean, Column, Integer, JSON, String, BigInteger
from sqlalchemy.dialects.postgresql import ARRAY

from app.domain import entities

_SCHEMA = "data"


class SmartContract(Base):
    __tablename__ = "smart_contract"
    __table_args__ = {"schema": _SCHEMA}

    event_id = Column(Integer, primary_key=True)
    collection_name = Column(String, nullable=False)
    crowdsale = Column(String, nullable=False)
    collection_address = Column(String, nullable=False)
    multisig = Column(String, nullable=False)
    is_presale = Column(Boolean, nullable=False)
    metadata_list = Column(ARRAY(String), nullable=False)
    price_per_token = Column(Integer, nullable=False)
    max_mint_per_user = Column(Integer, nullable=False)
    sale_size = Column(Integer, nullable=False)
    sale_currency = Column(JSON, nullable=False)
    start_time = Column(BigInteger, nullable=False)
    end_time = Column(BigInteger, nullable=False)

    def to_entity(self) -> entities.SmartContract:
        return entities.SmartContract(
            event_id=self.event_id,
            collection_name=self.collection_name,
            crowdsale=self.crowdsale,
            collection_address=self.collection_address,
            multisig=self.multisig,
            is_presale=self.is_presale,
            metadata_list=self.metadata_list,
            price_per_token=self.price_per_token,
            max_mint_per_user=self.max_mint_per_user,
            sale_size=self.sale_size,
            sale_currency=self.sale_currency,
            start_time=self.start_time,
            end_time=self.end_time
        )
