from typing import Optional
from pydantic import BaseModel, ConfigDict, HttpUrl, field_serializer
from synthetic_open_schema_model.base import Resource, CheckSpec
from synthetic_open_schema_model.v1beta1.http import Headers


class WebhookChannelSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: HttpUrl
    method: Optional[str] = "POST" 
    headers: Optional[Headers] = {}
    body: Optional[str] = None


    @field_serializer("url")
    def serialize_url(self, url: HttpUrl, _info):
        return str(url)

class WebhookChannel(Resource):
    model_config = ConfigDict(extra="forbid")

    spec: WebhookChannelSpec