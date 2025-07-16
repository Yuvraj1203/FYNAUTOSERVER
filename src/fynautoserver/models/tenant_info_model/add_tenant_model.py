from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

class TenantStatusEnum(str, Enum):
    pending = "Pending"
    ongoing = "On-Going"
    completed = "Completed"

class StepModel(BaseModel):
    id: int
    label: str
    status: TenantStatusEnum

class AddTenantModel(BaseModel):
    tenantId: str
    tenancyName: str
    tenantName: str
    tenantURL: str
    isAuth0Enable: bool
    isOktaEnabled: bool
    allowCommunityTemplateCreation: bool
    status: str
    step: Optional[int] = Field(default=1)
    steps: Optional[List[StepModel]] = None