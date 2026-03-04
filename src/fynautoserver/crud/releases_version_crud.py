from fynautoserver.schemas.index import TenantInfoSchema,ReleasesVersionTableSchema, StatusType, TenantReleaseStatusEnum, ReleaseResponseModel
from fynautoserver.models.index import TenantVersionProjection, ReleaseTenantsModel, ResponseModel, ReleaseTenantCreateModel
from typing import List
from fastapi import HTTPException, status
from beanie.odm.enums import SortDirection
from bson import ObjectId

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
                iosVersion=t.iosVersionName,
                matchBranch=t.matchBranch
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
async def get_releases_version_table(skipCount:int) -> List[ReleaseResponseModel]:
    try:
        documents = await ReleasesVersionTableSchema.find_all().sort([("_id", SortDirection.DESCENDING)]).skip(skipCount).limit(5).to_list()
        return [
            ReleaseResponseModel(
                id=str(doc.id),  # convert ObjectId → string
                version=doc.version,
                status=doc.status,
                tenants=doc.tenants
            )
            for doc in documents
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create_new_release_version_document"
        )
    
#to insert particular tenat in list
async def insert_particular_tenant_in_list( version:str,payload:ReleaseTenantCreateModel
) -> ResponseModel:

    try:
        tenant_data = {
            "id": str(ObjectId()),
            **payload.model_dump()
        }

        collection = ReleasesVersionTableSchema.get_motor_collection()
        result = await collection.update_one(
            {
                "version": version,
                "tenants": {
                    "$not": {
                        "$elemMatch": {"name": tenant_data["name"]}
                    }
                }
            },
            {
                "$push": {
                    "tenants": tenant_data
                }
            }
        )

        if result.modified_count == 0:
            return ResponseModel(
                success=False,
                result={"message": "Tenant with same name already exists"},
                status_code=400
            )
        return ResponseModel(
            success=True,
            result={"message": "Tenant added successfully"},
            status_code=200
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to insert_particular_tenant_in_list"
        )
    