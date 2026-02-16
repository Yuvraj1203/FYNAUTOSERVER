from pydantic import BaseModel, Field
from typing import List
from beanie import PydanticObjectId

class ReleaseTenantsModel(BaseModel):
    id: str
    name: str
    status: int
    androidVersion: str
    iosVersion: str

class StatusType(BaseModel):
    published: int
    onGoing: int
    pending: int
    failed: int

class TenantVersionProjection(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    appName: str
    androidVersionName: str
    iosVersionName: str

class ReleaseVersionTableResponse(BaseModel):
    id: str
    version: str
    status: StatusType
    tenants: List[ReleaseTenantsModel] = []