from fynautoserver.models.index import ResponseModel,BulkDeploymentPayloadModel, PipelineResponseModel, DeployTenantRequest
from fynautoserver.crud.bulk_deployment_crud import insert_data_for_bulk_deployment, delete_bulk_deployment_data, check_bulk_deployment_data_available, get_bulk_tenant_data
from fynautoserver.services.index import deploy_tenant_through_azure

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
                "android": "true",
                "ios": "true",
                "production": "false",
                "externalTester":"false",
                "buildApk": "true",
                "buildIpa": "true",
                "azureGitToken": bulk_deployment_data["azureGitToken"],
                **({"matchbranch": bulk_deployment_data["deploymentList"][0]["matchBranch"]} if bulk_deployment_data["deploymentList"][0].get("matchBranch") else {})
            }
        },
        bearerToken= bulk_deployment_data["azureBearerToken"]
    )

    if isInitialDeployment:
        # check tenantName make it inprogress and return
        get_zeroth_tenant = await bulk_deployment_data['deploymentList'][0] if bulk_deployment_data['deploymentList'] else None

        if get_zeroth_tenant:
            print(f"Zeroth tenant from list: {get_zeroth_tenant}")
            deploy = await deploy_tenant_through_azure(json_data)
            return deploy
        else:
            return ResponseModel(success=False, message="no deploy as no tenant found.", status_code=404, result=None)
    else:
        # update version in release list, 
        #update status in release list
        # delete zeroth tenant/tenant name from bulk_dep tenant list
        # call for second tenant to be deployed and make it inprogress

        pass
    return ResponseModel(success=True, message="Pipeline success response received", status_code=200, result=payload.model_dump())