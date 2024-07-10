from pydantic import BaseModel, ConfigDict

from .resources import ResourceMeta


class ResourcesIdGETResponse200(ResourceMeta):
    download_url: str

    model_config = ConfigDict(extra='forbid')
