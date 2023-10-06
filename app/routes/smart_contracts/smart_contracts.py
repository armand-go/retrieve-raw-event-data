from fastapi import APIRouter

from app.domain import usecases
from . import payloads


class SmartContracts:
    ep = APIRouter(prefix="/smartContracts")
    __smartContractUsecase: usecases.SmartContracts

    def __init__(self, smartContractUsecases: usecases.SmartContracts):
        SmartContracts.__smartContractUsecase = smartContractUsecases

    @staticmethod
    @ep.put("/{smart_contract_address}", response_model=payloads.SmartContract)
    async def update_event(id: str, modify: payloads.SmartContract.Update):
        sc = await SmartContracts.__smartContractUsecase.update_sc(
            id, modify.model_dump(exclude_unset=True)
        )
        return payloads.SmartContract.from_entity(sc)

    @staticmethod
    @ep.get("/{smart_contract_address}", response_model=payloads.SmartContract)
    async def retrieve_single_event(smart_contract_address: str):
        sc = await SmartContracts.__smartContractUsecase.retrieve_single_sc(
            smart_contract_address
        )
        return payloads.SmartContract.from_entity(sc)
