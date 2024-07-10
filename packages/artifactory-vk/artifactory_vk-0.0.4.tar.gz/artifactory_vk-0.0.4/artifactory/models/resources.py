from enum import Enum
from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class ResourceBase(BaseModel):
    file_name: str | None = None
    byte_size: int
    checksum_md5: str | None = None
    context: dict | None = None
    
    @field_validator('byte_size')
    @classmethod
    def gt0(cls, v: int) -> int:
        assert v > 0
        return v


class ResourceTTL(BaseModel):
    soft_ttl_s: int | None = None
    hard_ttl_s: int | None = None
    
    @field_validator('soft_ttl_s', 'hard_ttl_s')
    @classmethod
    def gt0_or_None(cls, v):
        assert (v is None or v > 0)
        return v


class StorageType(str, Enum):
    S3 = 'S3'
    YT = 'YT'


class ResourceS3Storage(BaseModel):
    endpoint: str
    region: str
    bucket: str
    key: str


class ResourceYTStorage(BaseModel):
    proxy: str
    path: str
    
    model_config = ConfigDict(extra='allow')


class ResourceStorage(BaseModel):
    storage_type: StorageType
    s3_storage_info: ResourceS3Storage | None = None
    yt_storage_info: ResourceYTStorage | None = None
    
    @model_validator(mode='after')
    def is_valid(self):
        if self.storage_type == StorageType.S3:
            assert self.s3_storage_info is not None
        if self.storage_type == StorageType.YT:
            assert self.yt_storage_info is not None
        return self


class ResourceMeta(ResourceBase, ResourceStorage, ResourceTTL):
    resource_id: str
    creation_ts: int
    has_ownership: bool
    draft_creation_ts: int | None = None
    last_access_ts: int
    is_removed: bool
    
    model_config = ConfigDict(extra='forbid')
