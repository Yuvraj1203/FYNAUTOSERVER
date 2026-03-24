from pydantic import BaseModel, Field
from typing import List, Dict, Any
from beanie import PydanticObjectId

class ReleaseTenantsModel(BaseModel):
    id: str
    name: str
    status: int
    androidStatus: int = 0
    iosStatus: int = 0
    androidVersion: str
    iosVersion: str
    matchBranch: str

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
    matchBranch: str

class ReleaseVersionTableResponse(BaseModel):
    id: str
    version: str
    status: StatusType
    tenants: List[ReleaseTenantsModel] = []

class DeployTenantRequest(BaseModel):
    body: Dict[str, Any]
    bearerToken: str