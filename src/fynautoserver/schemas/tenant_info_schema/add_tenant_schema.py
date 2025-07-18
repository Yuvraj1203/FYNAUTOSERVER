from enum import Enum
from pydantic import BaseModel , Field
from typing import List
from beanie import Document,Insert, Replace,before_event,Update

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

    @before_event(Insert)
    @before_event(Replace)
    @before_event(Update)
    async def set_status_from_steps(self):
        completed_steps = sum(1 for s in self.steps if s.status == "Completed")

        if completed_steps == 0:
            self.status = "Pending"
        elif completed_steps < 5:
            self.status = "On-Going"
        else:
            self.status = "Completed"