from typing import List

from pydantic import BaseModel


class SmartContract(BaseModel):
    event_id: int
    collection_name: str
    crowdsale: str
    collection_address: str
    multisig: str
    is_presale: bool
    metadata_list: List[str]
    price_per_token: int
    max_mint_per_user: int
    sale_size: int
    sale_currency: dict
    start_time: int
    end_time: int
