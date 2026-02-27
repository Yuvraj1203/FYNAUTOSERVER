from fynautoserver.models.index import ResponseModel
from fynautoserver.crud.releases_version_crud import get_releases_version_info_from_each_tenant, create_new_release_version_document,get_releases_version_table, check_if_already_exist_version, insert_particular_tenant_in_list
from fastapi import HTTPException, status
from fynautoserver.models.index import ReleaseTenantCreateModel


async def create_releases_version_service(version:str) -> ResponseModel:
    try:
        check_duplicated_version = await check_if_already_exist_version(version)
        if check_duplicated_version:
            return ResponseModel(success= True, result= {"status": 0, "message": "Version already exist"}, status_code= 200)

        get_all_tenants = await get_releases_version_info_from_each_tenant()
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