from pydantic import BaseModel
from http import HTTPStatus
from abc import ABC, abstractmethod
from typing import Optional, Any, List


class BaseException(Exception, ABC):
    status: int = HTTPStatus.IM_A_TEAPOT

    @abstractmethod
    def to_json(self) -> dict:
        """Format error to json"""


class Details(BaseModel):
    """
    Details represent a detailed error information to return to the user.
    """

    key: str
    message: str
    value: Optional[Any] = None


class ErrNotFound(BaseException):
    """
    ErrUnotFound has to be raised if data was expected but
    not does not exits.
    """

    status = HTTPStatus.NOT_FOUND

    def __init__(self, key: str):
        self.__key = key
        self.__error = "not found"
        super().__init__(f"NotFound{key.upper()}: {self.__error}")

    def to_json(self) -> dict:
        return {"key": self.__key, "error": self.__error}


class ErrUnexpected(BaseException):
    """
    ErrUnexpected represents global exception for errors that should not happen
    and we don't wish to provide information to end user.
    """

    status = HTTPStatus.INTERNAL_SERVER_ERROR

    def to_json(self) -> dict:
        return {
            "error": "something unexpected happened",
            "ERROR": "Internal error",
        }


class ErrInvalidData(BaseException):
    """
    ErrInvalidData propagate invalid data informations.
    """

    def __init__(
        self,
        key: str,
        error: str,
        details: List[Details] | None = None,
    ):
        self.__key = key
        self.__error = error
        self.__details = details
        self.status = HTTPStatus.BAD_REQUEST

        super().__init__(f"Invalid{key.upper()}: {error}")

    @property
    def main_error(self) -> str:
        return self.__error

    def to_json(self) -> dict:
        return {
            "key": self.__key,
            "error": self.__error,
            "details": [
                detail.model_dump() for detail in self.__details
            ] if self.__details else None,
        }
