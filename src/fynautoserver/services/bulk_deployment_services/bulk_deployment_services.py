from fynautoserver.models.index import ResponseModel,BulkDeploymentPayloadModel
from fynautoserver.crud.bulk_deployment_crud import insert_data_for_bulk_deployment

async def create_bulk_deployment_service(payload:BulkDeploymentPayloadModel) -> ResponseModel:
    create_data = await insert_data_for_bulk_deployment(payload)
    print(f"Bulk deployment creation response: {create_data}")

    if create_data:
        return ResponseModel(success=True, message="Bulk deployment created successfully", status_code=201, result=create_data)
    else:
        return ResponseModel(success=False, message="Failed to create bulk deployment", status_code=500, result=None)
