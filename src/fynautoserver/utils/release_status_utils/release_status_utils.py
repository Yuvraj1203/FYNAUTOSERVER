from fynautoserver.schemas.index import  TenantReleaseStatusEnum, StatusType, ReleaseTenantsModel

from typing import List

def calculate_release_status(tenants: List[ReleaseTenantsModel]) -> StatusType:
    
    published = 0
    onGoing = 0
    pending = 0
    failed = 0

    for tenant in tenants:
        if tenant.status == TenantReleaseStatusEnum.published:
            published += 1
        elif tenant.status == TenantReleaseStatusEnum.onGoing:
            onGoing += 1
        elif tenant.status == TenantReleaseStatusEnum.pending:
            pending += 1
        elif tenant.status == TenantReleaseStatusEnum.failed:
            failed += 1

    return StatusType(
        published=published,
        onGoing=onGoing,
        pending=pending,
        failed=failed
    )