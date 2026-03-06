from fastapi import APIRouter
from fynautoserver.models.index import ResponseModel, BulkDeploymentPayloadModel
from fynautoserver.services.index import create_bulk_deployment_service

bulk_deployment_router = APIRouter(
    prefix="/bulkDeployment",
    tags=["Bulk Deployment"]
)

@bulk_deployment_router.post("/createBulkDeployment", response_model=ResponseModel)
async def create_bulk_deployment(payload: BulkDeploymentPayloadModel) -> ResponseModel:
    create_bulk_deployment_response = await create_bulk_deployment_service(payload)
    return create_bulk_deployment_response