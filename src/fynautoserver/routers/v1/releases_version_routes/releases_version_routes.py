from fastapi import APIRouter
from fynautoserver.models.index import ResponseModel
from pydantic import BaseModel
from fynautoserver.services.index import create_releases_version_service, get_releases_version_service

releases_version_router = APIRouter()

class VersionPayload(BaseModel):
    version: str

@releases_version_router.post("/createReleasesVersion",response_model=ResponseModel)
async def create_releases_version(payload:VersionPayload) -> ResponseModel:
    create_version = await create_releases_version_service(payload.version)
    return create_version

@releases_version_router.get("/getReleasesVersion",response_model=ResponseModel)
async def get_releases_version(skipCount: int = 0) -> ResponseModel:
    get_releases_version = await get_releases_version_service(skipCount)
    return get_releases_version