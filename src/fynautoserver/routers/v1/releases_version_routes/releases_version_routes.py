from fastapi import APIRouter
from fynautoserver.models.index import ResponseModel,ReleaseTenantCreateModel, DeployTenantRequest, TenantStatusUpdateModel
from pydantic import BaseModel
from fynautoserver.services.index import create_releases_version_service, get_releases_version_service, add_custom_tenant_in_version, deploy_tenant_through_azure,check_progress_of_deployment, update_tenant_status_service
from typing import Any

releases_version_router = APIRouter()

class VersionPayload(BaseModel):
    version: str

@releases_version_router.post("/createReleasesVersion",response_model=ResponseModel)
async def create_releases_version(payload:VersionPayload) -> ResponseModel:
    create_version = await create_releases_version_service(payload.version)
    return create_version

@releases_version_router.get("/getReleasesVersion",response_model=ResponseModel)
async def get_releases_version(skipCount: int = 0) -> ResponseModel:
    get_releases_version = await get_releases_version_service(skipCount)
    return get_releases_version

@releases_version_router.put("/addCustomTenant", response_model=ResponseModel)
async def add_custom_tenant(version: str,payload: ReleaseTenantCreateModel) -> ResponseModel:
    add_version_tenant = await add_custom_tenant_in_version(version,payload)
    return add_version_tenant

@releases_version_router.post("/DeployTenants", response_model=ResponseModel)
async def deploy_tenant(payload:DeployTenantRequest) -> ResponseModel:
    deploy = await deploy_tenant_through_azure(payload)
    return deploy

@releases_version_router.get("/GetProgress",response_model=ResponseModel)
async def get_progress(token:str) -> ResponseModel:
    check_progress = await check_progress_of_deployment(token)
    return check_progress

@releases_version_router.put("/updateTenantStatus", response_model=ResponseModel)
async def update_tenant_status(version: str, payload: TenantStatusUpdateModel) -> ResponseModel:
    """
    Update tenant status and version.
    
    This endpoint:
    1. Searches for tenant by name in the specified version
    2. Updates the status of that tenant
    3. Based on status transition:
       - pending(0)/failed(3) -> inProgress(1): increment version
       - inProgress(1) -> failed(3): decrement version
    4. If android=true: update android version
    5. If ios=true: update ios version
    """
    update_status = await update_tenant_status_service(version, payload)
    return update_status
