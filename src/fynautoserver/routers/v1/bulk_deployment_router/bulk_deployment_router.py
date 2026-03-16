from fastapi import APIRouter
from fynautoserver.models.index import ResponseModel, BulkDeploymentPayloadModel, PipelineResponseModel
from fynautoserver.services.index import create_bulk_deployment_service,delete_bulk_deployment_service, get_available_bulk_deployment_data_service, on_pipeline_success_service

bulk_deployment_router = APIRouter(
    prefix="/bulkDeployment",
    tags=["Bulk Deployment"]
)

@bulk_deployment_router.post("/createBulkDeployment", response_model=ResponseModel)
async def create_bulk_deployment(payload: BulkDeploymentPayloadModel) -> ResponseModel:
    create_bulk_deployment_response = await create_bulk_deployment_service(payload)
    return create_bulk_deployment_response

@bulk_deployment_router.delete("/deleteBulkDeploymentData",response_model=ResponseModel)
async def delete_bulk_deployment_data() -> ResponseModel:
    delete_bulk_deployment_data_response = await delete_bulk_deployment_service()
    return delete_bulk_deployment_data_response

@bulk_deployment_router.get("/DeploymentDataAvailable",response_model=ResponseModel)
async def check_bulk_deployment_data_available() -> ResponseModel:
    is_data_available = await get_available_bulk_deployment_data_service()
    return is_data_available

@bulk_deployment_router.post("/OnPipelineSuccess",response_model=ResponseModel)
async def on_pipeline_success(payload: PipelineResponseModel) -> ResponseModel:
    on_pipeline_success_response = await on_pipeline_success_service(payload)
    return on_pipeline_success_response