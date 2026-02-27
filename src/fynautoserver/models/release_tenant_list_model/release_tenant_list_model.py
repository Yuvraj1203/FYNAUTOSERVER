from pydantic import BaseModel
from typing import List

class ReleaseTenantCreateModel(BaseModel):
    name: str
    status: int
    androidVersion: str
    iosVersion: str
    matchBranch: str

class ReleaseTenantsModel(BaseModel):
    id: str
    name: str
    status: int
    androidVersion: str
    iosVersion: str
    matchBranch: str

class ReleaseTenantsListModel(BaseModel):
    id: str
    version: str
    tenants: List[ReleaseTenantsModel]