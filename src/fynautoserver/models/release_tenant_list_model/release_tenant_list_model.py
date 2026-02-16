from pydantic import BaseModel
from typing import List

class ReleaseTenantsModel(BaseModel):
    id: str
    name: str
    status: int
    androidVersion: str
    iosVersion: str

class ReleaseTenantsListModel(BaseModel):
    id: str
    version: str
    tenants: List[ReleaseTenantsModel]