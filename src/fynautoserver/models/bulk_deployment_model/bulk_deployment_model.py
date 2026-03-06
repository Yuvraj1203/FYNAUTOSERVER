from pydantic import BaseModel
from typing import List

class BulkDeploymentListModel(BaseModel):
    id: str
    tenantName: str
    matchBranch: str

class BulkDeploymentPayloadModel(BaseModel):
    azureGitToken: str
    azureBearerToken: str
    gitBranch: str
    onlyTestflight: bool = False
    deploymentList: List[BulkDeploymentListModel]

