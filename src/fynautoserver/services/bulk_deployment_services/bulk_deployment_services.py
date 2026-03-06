from fynautoserver.models.index import ResponseModel,BulkDeploymentPayloadModel
from fynautoserver.crud.bulk_deployment_crud import insert_data_for_bulk_deployment, delete_bulk_deployment_data, check_bulk_deployment_data_available

async def create_bulk_deployment_service(payload:BulkDeploymentPayloadModel) -> ResponseModel:
    create_data = await insert_data_for_bulk_deployment(payload)
    print(f"Bulk deployment creation response: {create_data}")

    if create_data:
        return ResponseModel(success=True, message="Bulk deployment created successfully", status_code=201, result=create_data)
    else:
        return ResponseModel(success=False, message="Failed to create bulk deployment", status_code=500, result=None)

async def delete_bulk_deployment_service() -> ResponseModel:
    delete_data = await delete_bulk_deployment_data()

    if delete_data:
        return ResponseModel(success=True, message="Bulk deployment data deleted successfully", status_code=200, result=delete_data)
    else:
        return ResponseModel(success=False, message="Failed to delete bulk deployment data", status_code=500, result=None)

async def get_available_bulk_deployment_data_service() -> ResponseModel:
    is_data_available = await check_bulk_deployment_data_available()
    return ResponseModel(success=True, message="Bulk deployment data is available", status_code=200, result=is_data_available)
    