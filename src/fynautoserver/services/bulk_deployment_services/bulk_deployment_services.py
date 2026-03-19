from fynautoserver.models.index import ResponseModel,BulkDeploymentPayloadModel, PipelineResponseModel, DeployTenantRequest
from fynautoserver.crud.bulk_deployment_crud import insert_data_for_bulk_deployment, delete_bulk_deployment_data, check_bulk_deployment_data_available, get_bulk_tenant_data, update_release_tenant_version_and_status_service, delete_bulk_deployment_zeroth
from fynautoserver.services.index import deploy_tenant_through_azure
from fynautoserver.schemas.index import TenantReleaseStatusEnum
from fynautoserver.schemas.index import BulkDeploymentListSchema

async def create_bulk_deployment_service(payload:BulkDeploymentPayloadModel) -> ResponseModel:
    create_data = await insert_data_for_bulk_deployment(payload)
    print(f"Bulk deployment creation response: {create_data}")

    if create_data:
        on_pipeline_success_service_response = await on_pipeline_success_service(PipelineResponseModel(
            android=False,
            ios=False,
        ))
        print(f"On pipeline success service response: {on_pipeline_success_service_response}")
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

async def on_pipeline_success_service(payload: PipelineResponseModel) -> ResponseModel:
    # You can add any additional logic here if needed before returning the response
    isInitialDeployment = payload.android == False and payload.ios == False

    bulk_deployment_data = await get_bulk_tenant_data()

    if not bulk_deployment_data:
        return ResponseModel(success=False, message="No bulk deployment data found", status_code=404, result=None)

    bulk_deployment_data = bulk_deployment_data.model_dump()  

    json_data = DeployTenantRequest(
        body= {
            "resources": {
                "repositories": {
                    "self": {
                      "refName": f"refs/heads/{bulk_deployment_data['gitBranch']}"
                    }
                }
            },
            "templateParameters": {
                "tenant": bulk_deployment_data["deploymentList"][0]["tenantName"],
                "android": "true" if bulk_deployment_data["onlyTestflight"] == False else "false",
                "ios": "true",
                "production": "false",
                "externalTester":"false",
                "buildApk": "true" if bulk_deployment_data["onlyTestflight"] == False else "false",
                "buildIpa": "true",
                "azureGitToken": bulk_deployment_data["azureGitToken"],
                **({"matchbranch": bulk_deployment_data["deploymentList"][0]["matchBranch"]} if bulk_deployment_data["deploymentList"][0].get("matchBranch") else {}),
                "deployAll": "true",
            }
        },
        bearerToken= bulk_deployment_data["azureBearerToken"]
    )

    # get_zeroth_tenant = bulk_deployment_data['deploymentList'][0] if bulk_deployment_data['deploymentList'] else None

    get_zeroth_tenant = (
    BulkDeploymentListSchema(**bulk_deployment_data["deploymentList"][0])
    if bulk_deployment_data["deploymentList"]
    else None
)

    if isInitialDeployment:
        # check tenantName make it inprogress and return

        if get_zeroth_tenant:
            print(f"Zeroth tenant from list: {get_zeroth_tenant}")
            update_release_list = await update_release_tenant_version_and_status_service(
                tenant_info= get_zeroth_tenant,
                status = TenantReleaseStatusEnum.onGoing 
            )

            # return ResponseModel(success=False, message="no deploy as no tenant found.", status_code=404, result=None)
            deploy = await deploy_tenant_through_azure(json_data)

            #update status in tenants in releases_version_table which have same name as  bulk_deployment_data['deploymentList'][0] and put status inprogress

            return deploy
        else:
            return ResponseModel(success=False, message="no deploy as no tenant found.", status_code=404, result=None)
    else:
        # update version in tenants in releases_version_table which have same name as  bulk_deployment_data['deploymentList'][0] and put version from payload android version and iosVersion
        if get_zeroth_tenant:
            update_release_list = await update_release_tenant_version_and_status_service(
                tenant_info= get_zeroth_tenant,
                iosVersion= payload.iosVersion,
                androidVersion= payload.androidVersion,
                status = TenantReleaseStatusEnum.published if payload.android == True and payload.ios == True else TenantReleaseStatusEnum.failed
            )

            # delete zeroth element from deploymentLIst in bulk_deployment
            if update_release_list:
                is_zeroth_deleted = await delete_bulk_deployment_zeroth() 

                # call this function again 
                if is_zeroth_deleted:
                    return await on_pipeline_success_service(payload)
                
                return ResponseModel(success=True, message="Bulk deployment updated successfully", status_code=200, result={"is_zeroth_deleted": is_zeroth_deleted})
            else:
                return ResponseModel(success=False, message="no deploy as no tenant found.", status_code=404, result=None)
        else:
            return ResponseModel(success=False, message="no deploy as no tenant found.", status_code=404, result=None)