from beanie import Document
from pydantic import BaseModel
from enum import IntEnum
from typing import List
from fynautoserver.models.index import ReleaseTenantsModel

class TenantReleaseStatusEnum(IntEnum):
    pending = 0
    onGoing = 1
    published = 2
    failed = 3

class StatusType(BaseModel):
    published: int
    onGoing: int
    pending: int
    failed: int

class ReleasesVersionTableSchema(Document):
    version: str
    status: StatusType
    tenants: List[ReleaseTenantsModel] 

    class Settings:
        name = "releases_version_table"