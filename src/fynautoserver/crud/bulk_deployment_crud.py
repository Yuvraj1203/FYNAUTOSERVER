from fynautoserver.models.index import BulkDeploymentPayloadModel
from fynautoserver.schemas.index import BulkDeploymentSchema, BulkDeploymentListSchema
from bson import ObjectId

async def insert_data_for_bulk_deployment(payload:BulkDeploymentPayloadModel) -> bool:
    try:
        await BulkDeploymentSchema.find_all().delete()

        bulk_deployment_data = BulkDeploymentSchema(
            azureGitToken=payload.azureGitToken,
            azureBearerToken=payload.azureBearerToken,
            gitBranch=payload.gitBranch,
            onlyTestflight=payload.onlyTestflight,
            deploymentList=[BulkDeploymentListSchema(**deployment.model_dump()) for deployment in payload.deploymentList]
        )
        await bulk_deployment_data.insert()
        return True
    except Exception as e:
        print(f"Error inserting bulk deployment data: {e}") 
        return False

async def delete_bulk_deployment_data() -> bool:
    try:
        await BulkDeploymentSchema.find_all().delete()
        return True
    except Exception as e:
        print(f"Error deleting bulk deployment data: {e}") 
        return False
    
async def check_bulk_deployment_data_available() -> int:
    try:
        data = await BulkDeploymentSchema.find_one()
        length = len(data.deploymentList) if data and data.deploymentList else 0
        return length
    except Exception as e:
        print(f"Error checking bulk deployment data availability: {e}") 
        return 0