from enum import Enum
from typing import Optional

from ..base import Check, CheckSpec, BaseExpect, Time
from pydantic import ConfigDict, HttpUrl, field_serializer


Headers = dict[str, str]


class HttpExpectType(str, Enum):
    duration = "duration"
    size = "size"
    statusCode = "statusCode"
    text = "text"
    headers = "headers"


class HttpExpect(BaseExpect):
    type: HttpExpectType
    type: str


HttpExpectList = list[HttpExpect]


class HttpCheckSpec(CheckSpec):
    model_config = ConfigDict(extra="forbid")

    url: HttpUrl
    method: Optional[str] = "GET"
    headers: Optional[Headers] = {}
    checks: Optional[HttpExpectList] = []


    @field_serializer("url")
    def serialize_url(self, url: HttpUrl, _info):
        return str(url)


class HttpCheck(Check):
    model_config = ConfigDict(extra="forbid")

    spec: HttpCheckSpec
