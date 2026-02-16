from fynautoserver.schemas.index import TenantInfoSchema,ReleasesVersionTableSchema, StatusType, TenantReleaseStatusEnum
from fynautoserver.models.index import TenantVersionProjection, ReleaseTenantsListModel, ReleaseTenantsModel, ReleaseTenantsListModel
from typing import List
from fastapi import HTTPException, status
from beanie.odm.enums import SortDirection

async def check_if_already_exist_version(version:str) -> bool:
    try:
        existing_version = await ReleasesVersionTableSchema.find_one(ReleasesVersionTableSchema.version == version)
        if existing_version:
            return True
        return False
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check for existing version"
        )

async def get_releases_version_info_from_each_tenant() -> List[ReleaseTenantsModel]:

    try:
        tenants = await TenantInfoSchema.find_all().project(TenantVersionProjection).to_list()
        return [
            ReleaseTenantsModel(
                id=str(t.id),
                name=t.appName,
                status=TenantReleaseStatusEnum.pending,
                androidVersion=t.androidVersionName,
                iosVersion=t.iosVersionName
            )
            for t in tenants
        ]
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get_releases_version_info_from_each_tenant"
        )
    
async def create_new_release_version_document(allTenantsInThisVersion:List[ReleaseTenantsModel],totalTenants:int,version:str) -> ReleasesVersionTableSchema:
    try:
        doc = ReleasesVersionTableSchema(
                version=version,
                status=  StatusType(
                    pending=totalTenants,
                    onGoing=0,
                    published=0,
                    failed=0
                ),
                tenants = allTenantsInThisVersion
            )
        await doc.insert()
        return doc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to insert tenant versions"
        )
    
#getting accordian title data--in next process by id we will get the tenants list which is there in this release
async def get_releases_version_table(skipCount:int) -> List[ReleasesVersionTableSchema]:
    try:
        return await ReleasesVersionTableSchema.find_all().sort([("_id", SortDirection.DESCENDING)]).skip(skipCount).limit(5).to_list()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create_new_release_version_document"
        )
    
# to get the particular tenants list for each releases version
# async def get_particular_tenants_list(particular_id:str) -> ReleaseTenantsListModel | None:
#     particular_tenants = await ReleaseTenantsList.get(particular_id)
    

#     if not particular_tenants:
#         return None

#     return ReleaseTenantsListModel(
#         id=str(particular_tenants.id),         
#         version=particular_tenants.version,
#         tenants=particular_tenants.tenants
#     )