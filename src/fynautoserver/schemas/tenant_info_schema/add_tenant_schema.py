from enum import Enum
from pydantic import BaseModel , Field
from typing import List
from beanie import Document

class TenantStatusEnum(str, Enum):
    pending = "Pending"
    ongoing = "On-Going"
    completed = "Completed"

class StepModel(BaseModel):
    id: int
    label: str
    status: TenantStatusEnum

DEFAULT_STEPS: List[StepModel] = [
    StepModel(id=1, label="Tenant Info", status=TenantStatusEnum.ongoing),
    StepModel(id=2, label="File Configs", status=TenantStatusEnum.pending),
    StepModel(id=3, label="Theme", status=TenantStatusEnum.pending),
    StepModel(id=4, label="Font Embeding", status=TenantStatusEnum.pending),
    StepModel(id=5, label="Icon Generator", status=TenantStatusEnum.pending),
]

class AddTenantSchema(Document):
    tenantId: str
    tenancyName: str
    tenantName: str
    tenantURL: str
    isAuth0Enable: bool
    isOktaEnabled: bool
    allowCommunityTemplateCreation: bool
    status: str
    step : int = Field(default=1)
    steps : List[StepModel]

    class Settings:
        name = 'tenant_details'