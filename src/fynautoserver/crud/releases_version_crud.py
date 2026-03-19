from fynautoserver.schemas.index import TenantInfoSchema,ReleasesVersionTableSchema, StatusType, TenantReleaseStatusEnum, ReleaseResponseModel
from fynautoserver.models.index import TenantVersionProjection, ReleaseTenantsModel, ResponseModel, ReleaseTenantCreateModel, TenantStatusUpdateModel, increment_version, decrement_version
from typing import List, Optional
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

async def get_custom_created_tenants() -> List[ReleaseTenantsModel]:
    try:
        # Fetch all versions and extract custom tenants
        version = await ReleasesVersionTableSchema.find_one(sort=[("_id",-1)])
        if not version:
            return []
        
        custom_tenants = []
        for tenant in version.tenants:
            if tenant.id and tenant.name:  # Assuming custom tenants have these fields
                custom_tenants.append(
                    ReleaseTenantsModel(
                        id=tenant.id,
                        name=tenant.name,
                        status=TenantReleaseStatusEnum.pending,
                        androidVersion=tenant.androidVersion,
                        iosVersion=tenant.iosVersion,
                        matchBranch=tenant.matchBranch
                    )
                )
        return custom_tenants
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get_custom_created_tenants"
        )
    
async def create_new_release_version_document(allTenantsInThisVersion:List[ReleaseTenantsModel],totalTenants:int,version:str) -> ReleasesVersionTableSchema:
    try:
        # Calculate status counts from tenants list (single source of truth)
        pending_count = sum(1 for t in allTenantsInThisVersion if t.status == 0)
        on_going_count = sum(1 for t in allTenantsInThisVersion if t.status == 1)
        published_count = sum(1 for t in allTenantsInThisVersion if t.status == 2)
        failed_count = sum(1 for t in allTenantsInThisVersion if t.status == 3)
        
        doc = ReleasesVersionTableSchema(
                version=version,
                status=StatusType(
                    pending=pending_count,
                    onGoing=on_going_count,
                    published=published_count,
                    failed=failed_count
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


async def update_tenant_status_and_version(
    version: str,
    tenant_name: str,
    new_status: int,
    increment_android: bool = False,
    increment_ios: bool = False
) -> Optional[ReleaseTenantsModel]:
    """
    Update tenant status and version based on status transition.
    
    Logic:
    - pending(0)/failed(3) -> inProgress(1): increment version
    - inProgress(1) -> failed(3): decrement version
    
    Args:
        version: The version to search for
        tenant_name: The tenant name to update
        new_status: The new status to set (0=pending, 1=onGoing, 2=published, 3=failed)
        increment_android: Whether to increment android version
        increment_ios: Whether to increment iOS version
    
    Returns:
        Updated tenant data or None if not found
    """
    try:
        # Find the document with the given version
        doc = await ReleasesVersionTableSchema.find_one(ReleasesVersionTableSchema.version == version)
        
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Version {version} not found"
            )
        
        # Find the tenant in the list
        tenant_found = None
        tenant_index = -1
        old_status = None
        
        for i, tenant in enumerate(doc.tenants):
            if tenant.name.lower() == tenant_name.lower():
                tenant_found = tenant
                tenant_index = i
                old_status = tenant.status
                break
        
        if not tenant_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tenant with name '{tenant_name}' not found in version {version}"
            )
        
        # Determine if we should increment or decrement version based on status transition
        should_increment = False
        should_decrement = False
        
        # pending(0) or failed(3) -> inProgress(1): increment version
        if old_status in [0, 3] and new_status == 1:
            should_increment = True
        # inProgress(1) -> failed(3): decrement version
        elif old_status == 1 and new_status == 3:
            should_decrement = True
        
        # Update the tenant's android version if requested
        updated_android_version = tenant_found.androidVersion
        updated_ios_version = tenant_found.iosVersion
        
        if increment_android:
            if should_increment:
                updated_android_version = increment_version(tenant_found.androidVersion)
            elif should_decrement:
                updated_android_version = decrement_version(tenant_found.androidVersion)
        
        if increment_ios:
            if should_increment:
                updated_ios_version = increment_version(tenant_found.iosVersion)
            elif should_decrement:
                updated_ios_version = decrement_version(tenant_found.iosVersion)
        
        # Update the tenant in the document
        doc.tenants[tenant_index] = ReleaseTenantsModel(
            id=tenant_found.id,
            name=tenant_found.name,
            status=new_status,
            androidVersion=updated_android_version,
            iosVersion=updated_ios_version,
            matchBranch=tenant_found.matchBranch
        )
        
        # Calculate status counts from tenants list (single source of truth)
        pending_count = sum(1 for t in doc.tenants if t.status == 0)
        on_going_count = sum(1 for t in doc.tenants if t.status == 1)
        published_count = sum(1 for t in doc.tenants if t.status == 2)
        failed_count = sum(1 for t in doc.tenants if t.status == 3)
        
        # Update status with computed values
        doc.status = StatusType(
            pending=pending_count,
            onGoing=on_going_count,
            published=published_count,
            failed=failed_count
        )
        
        await doc.save()
        
        return doc.tenants[tenant_index]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update tenant status: {str(e)}"
        )
    