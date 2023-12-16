from fastapi import HTTPException
from ipaddress import IPv4Address

from pydantic import BaseModel, ValidationError, field_validator
from pydantic.networks import AnyHttpUrl

from enum import Enum
from http.client import responses


class LogBase(BaseModel):
    """Входящая строка."""
    log: str


class RequestTypeEnum(Enum):
    GET = "GET"
    POST = "POST"
    PUT = 'PUT'
    PATCH = "PATCH"
    DELETE = "DELETE"


class LogCheck(BaseModel):
    """Валидация данных."""
    ip_address: IPv4Address
    http_method: RequestTypeEnum
    uri: AnyHttpUrl
    http_status_code: int

    @field_validator('http_status_code')
    @classmethod
    def http_status_code(cls, code: str) -> int:
        """Валидация переданного статуса http-кода."""
        http_status_code = list(map(int, responses))
        if int(code) not in http_status_code:
            raise HTTPException(status_code=418, detail='Что-то пошло не так')
        return int(code)


async def validate(data) -> LogCheck:
    """Валидация входящих данных."""
    try:
        data = {
            "ip_address": data[0],
            "http_method": data[1],
            "uri": data[2],
            "http_status_code": data[3]
        }
        return LogCheck.model_validate(data)
    except (ValidationError, ValueError, IndexError):
        raise HTTPException(status_code=418, detail='Что-то пошло не так')
