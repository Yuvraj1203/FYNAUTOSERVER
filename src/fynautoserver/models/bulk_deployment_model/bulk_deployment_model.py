from pydantic import BaseModel
from typing import List, Optional

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

class PipelineResponseModel(BaseModel):
    tenantName: Optional[str] = None
    android: bool = False
    ios: bool = False
    androidVersion: Optional[str] = None
    iosVersion: Optional[str] = None
    initialRun: Optional[bool] = False

