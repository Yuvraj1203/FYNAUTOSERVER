from fynautoserver.models.index import ResponseModel, DeployTenantRequest, TenantStatusUpdateModel
from fynautoserver.crud.releases_version_crud import get_releases_version_info_from_each_tenant, get_custom_created_tenants, create_new_release_version_document,get_releases_version_table, check_if_already_exist_version, insert_particular_tenant_in_list, update_tenant_status_in_release_list
from fastapi import HTTPException, status
from fynautoserver.schemas.index import ReleasesVersionTableSchema, TenantReleaseStatusEnum, StatusType, PipelinePayload
from fynautoserver.models.index import ReleaseTenantCreateModel
from typing import List
import httpx, base64


async def create_releases_version_service(version:str) -> ResponseModel:
    try:
        check_duplicated_version = await check_if_already_exist_version(version)
        if check_duplicated_version:
            return ResponseModel(success= True, result= {"status": 0, "message": "Version already exist"}, status_code= 200)

        #take tenants from list in dashboard
        already_created_tenants = await get_releases_version_info_from_each_tenant()

        #take tenant which are added customaly by add tenant from prev release list
        custom_created_tenants = await get_custom_created_tenants()

        tenant_map = {}

        # dashboard tenants
        for tenant in already_created_tenants:
            tenant_map[tenant.id] = tenant

        # add custom tenants if not already present
        for tenant in custom_created_tenants:
            if tenant.id not in tenant_map:
                tenant_map[tenant.id] = tenant

        get_all_tenants = list(tenant_map.values())
        total_tenant = len(get_all_tenants)
        await create_new_release_version_document(get_all_tenants,total_tenant,version)
        return ResponseModel(success= True, result= {"status": 1, "message": "Version created successfully"}, status_code= 200)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create_releases_version_service"
        )
    
async def get_releases_version_service(skipCount:int) -> ResponseModel:
    try:
        get_releases_versions = await get_releases_version_table(skipCount)
        if len(get_releases_versions) == 0:
            return ResponseModel(success= True, result=(), status_code= 200)
        

        return ResponseModel(success= True, result= get_releases_versions, status_code= 200)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get_releases_version_service"
        )
    

async def add_custom_tenant_in_version(version:str,payload:ReleaseTenantCreateModel) -> ResponseModel:
    try:
        #check is the version id available
        isExiting = await check_if_already_exist_version(version)
        if not isExiting:
            return ResponseModel(success= False, result= {"status": 0, "message": "Version not found"},status_code= 200)

        #check is the tenant id already exist
        isTenantExist = await insert_particular_tenant_in_list(version,payload)
        return ResponseModel(success= True, result= {"status": 1, "message": "Tenant added successfully"}, status_code= 200)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add_custom_tenant_in_version"
        )

async def deploy_tenant_through_azure(payload:DeployTenantRequest) -> ResponseModel:
    try:
        #update status in release list
        template_params = payload.body.get("templateParameters", {})

        android = template_params.get("android")
        ios = template_params.get("ios")

        tenant_name = template_params.get("tenant")

        android_bool = android == "true"
        ios_bool = ios == "true"

        release_ver_table = await ReleasesVersionTableSchema.find_one(sort=[("_id",-1)])

        if not release_ver_table:
            return ResponseModel(success= False, result= {"status": 0, "message": "Release version not found"}, status_code= 404)
        
        tenant = next(
            (t for t in release_ver_table.tenants if t.name == tenant_name),
            None
        )

        if not tenant:
            return ResponseModel(success= False, result= {"status": 0, "message": "Tenant not found"}, status_code= 404)

        if android_bool:
            #update tenant to in progress
            tenant.androidStatus = TenantReleaseStatusEnum.onGoing

        if ios_bool:
            #update tenant to in progress
            tenant.iosStatus = TenantReleaseStatusEnum.onGoing

        print("release_ver_table=>",release_ver_table)
        await release_ver_table.save()

        # return ResponseModel(success= True, result= {"status": 1, "message": "Tenant deployed successfully"}, status_code= 200)

        print(f"Deploying tenant through Azure with payload: {payload}")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url="https://dev.azure.com/kansoftware/Thoroughbred%20Apps/_apis/pipelines/103/runs",
                params={"api-version": "7.1-preview.1"},
                json=payload.body,
                headers={"Authorization": f"Bearer {payload.bearerToken}",
                         "Content-Type": "application/json"},
                timeout=10.0
            )
        return ResponseModel(success= True, result= {"status": 1, "message": "Tenant deployed successfully","data":response.json()}, status_code= 200)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deploy_tenant_through_azure"
        )

async def check_progress_of_deployment(token:str) -> ResponseModel:
    try:
        async with httpx.AsyncClient() as client:
            encoded_pat = base64.b64encode(f":{token}".encode()).decode()

            headers = {
                "Authorization": f"Basic {encoded_pat}"
            }
            response = await client.get(
                url="https://dev.azure.com/kansoftware/Thoroughbred%20Apps/_apis/pipelines/103/runs?api-version=7.1-preview.1",
                timeout=10.0,
                headers=headers
            )
            response_data = response.json()
            if(response_data["value"][0]["state"] == "inProgress"):
                return ResponseModel(success= True, result= {"status": response_data["value"][0]["state"], "message": "Deployment is in progress","tenant":response_data["value"][0]["templateParameters"]["tenant"]}, status_code= 200)
            else:
                if(response_data["value"][0]["result"] == "failed"):
                    return ResponseModel(success= True, result= {"status": response_data["value"][0]["result"], "message": "Deployment is failed","tenant":response_data["value"][0]["templateParameters"]["tenant"]}, status_code= 200)
                return ResponseModel(success= True, result= {"status": response_data["value"][0]["result"], "message": "Deployment is completed","tenant":response_data["value"][0]["templateParameters"]["tenant"]}, status_code= 200)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check_progress_of_deployment"
        )


async def update_tenant_status_service(
    version: str,
    payload: TenantStatusUpdateModel
) -> ResponseModel:
    
    #check if version available
    isValidReleaseVersion = await check_if_already_exist_version(version)

    if isValidReleaseVersion == False:
        return ResponseModel(success= False, result= {"status": 0, "message": "Version not found"},status_code=404)
    
    #check status is valid
    if payload.status < 0 or payload.status > 4:
        return ResponseModel(success= False, result= {"status": 0, "message": "Invalid status"},status_code=404)
    
    #check if the name is in the release version list and update status
    return await update_tenant_status_in_release_list(version,payload)
    


async def deploy_single_tenant_service(payload:DeployTenantRequest) -> ResponseModel:

    #save payload
    template_params = payload.body.get("templateParameters", {})

    android = template_params.get("android")
    ios = template_params.get("ios")

    tenant_name = template_params.get("tenant")

    android_bool = android == "true"
    ios_bool = ios == "true"

    await PipelinePayload(
        tenantName=tenant_name,
        forAndroid=android_bool,
        forIos=ios_bool
    ).save()

    deploy = await deploy_tenant_through_azure(payload)
    return deploy