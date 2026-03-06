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