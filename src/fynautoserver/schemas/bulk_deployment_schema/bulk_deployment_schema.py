from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from typing import List
from bson import ObjectId

class BulkDeploymentListSchema(BaseModel):
    id: str
    tenantName: str
    matchBranch: str

class BulkDeploymentSchema(Document):
    azureGitToken: str
    azureBearerToken: str
    gitBranch: str
    onlyTestflight: bool = False
    deploymentList: List[BulkDeploymentListSchema]

    class Settings:
        name = "bulk_deployment"

