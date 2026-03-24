from beanie import Document, before_event, after_event, Insert, Replace, Save
from pydantic import BaseModel, model_validator
from enum import IntEnum
from typing import List

class TenantReleaseStatusEnum(IntEnum):
    pending = 0
    onGoing = 1
    published = 2
    failed = 3

class StatusType(BaseModel):
    published: int
    onGoing: int
    pending: int
    failed: int


class ReleaseTenantsModel(BaseModel):
    id: str
    name: str
    status: int
    androidStatus: int = 0
    iosStatus: int = 0
    androidVersion: str
    iosVersion: str
    matchBranch: str

    @model_validator(mode="after")
    def update_status(self) -> "ReleaseTenantsModel":
        # If both statuses are equal
        if self.androidStatus == self.iosStatus:
            self.status = self.androidStatus
        else:
            # custom rule when different
            if TenantReleaseStatusEnum.failed in [self.androidStatus, self.iosStatus]:
                self.status = TenantReleaseStatusEnum.failed
            elif TenantReleaseStatusEnum.onGoing in [self.androidStatus, self.iosStatus]:
                self.status = TenantReleaseStatusEnum.onGoing
            else:
                self.status = TenantReleaseStatusEnum.pending

        return self

class ReleaseResponseModel(BaseModel):
    id: str
    version: str
    status: StatusType
    tenants: List[ReleaseTenantsModel]

class ReleasesVersionTableSchema(Document):
    version: str
    status: StatusType
    tenants: List[ReleaseTenantsModel] 

    class Settings:
        name = "releases_version_table"

    @before_event([Insert, Replace, Save])
    def update_release_status(self) -> None:
        published = 0
        onGoing = 0
        pending = 0
        failed = 0

        for tenant in self.tenants:
            if tenant.status == TenantReleaseStatusEnum.published:
                published += 1
            elif tenant.status == TenantReleaseStatusEnum.onGoing:
                onGoing += 1
            elif tenant.status == TenantReleaseStatusEnum.pending:
                pending += 1
            elif tenant.status == TenantReleaseStatusEnum.failed:
                failed += 1

        self.status = StatusType(
            published=published,
            onGoing=onGoing,
            pending=pending,
            failed=failed
        )