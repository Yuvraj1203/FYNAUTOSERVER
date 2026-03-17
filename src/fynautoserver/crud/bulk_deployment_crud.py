from fynautoserver.models.index import BulkDeploymentPayloadModel
from fynautoserver.schemas.index import BulkDeploymentSchema, BulkDeploymentListSchema, TenantReleaseStatusEnum, ReleasesVersionTableSchema, BulkDeploymentListSchema
from bson import ObjectId
from typing import Any

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

async def get_bulk_tenant_data() ->  BulkDeploymentSchema | None:
    try:
        data = await BulkDeploymentSchema.find_one()
        if data:
            return data
        else:
            print("No deployment data available to get tenant name.")
            return None
    except Exception as e:
        print(f"Error getting zeroth tenant from list: {e}") 
        return None
    
async def update_release_tenant_version_and_status_service(
    tenant_info: BulkDeploymentListSchema,
    status: TenantReleaseStatusEnum,
    iosVersion: str | None = None,
    androidVersion: str | None = None,
) -> bool:
    try:
        releases_version = await ReleasesVersionTableSchema.find_one(sort=[("_id", -1)])
        if not releases_version:
            print("No release version found to update tenant info.")
            return False
        
        print(f"this is release version {releases_version}")
        #now in this i want to change version and status which matches the tenant name and update the db
        # loop through tenants
        for tenant in releases_version.tenants:
            if tenant.name == tenant_info.tenantName:
                if iosVersion:
                    tenant.iosVersion = iosVersion
                if androidVersion:
                    tenant.androidVersion = androidVersion    
                tenant.status = status
                break

        # save the parent document
        await releases_version.save()

        return True
    except Exception as e:
        print(f"Error updating tenant release: {e}")
        return False

async def delete_bulk_deployment_zeroth() -> bool:
    try:
        data = await BulkDeploymentSchema.find_one()
        if data and data.deploymentList:
            data.deploymentList.pop(0)  # Remove the zeroth element
            await data.save()  # Save the updated document
            return True
        else:
            print("No deployment data available to delete zeroth tenant.")
            return False
    except Exception as e:
        print(f"Error deleting zeroth tenant from list: {e}") 
        return False