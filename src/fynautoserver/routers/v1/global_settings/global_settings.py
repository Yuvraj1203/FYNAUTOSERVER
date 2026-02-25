from fastapi import APIRouter
from fynautoserver.utils.index import create_response
from fynautoserver.crud.global_settings_crud import save_global_settings, get_global_settings
from pydantic import BaseModel
from typing import Optional


router = APIRouter()


class GlobalSettingsPayload(BaseModel):
    azureGitCred: Optional[str] = None
    azureBearerToken: Optional[str] = None
    branch: Optional[str] = None


@router.post('/globalSettings', response_model=dict)
async def set_global_settings(payload: GlobalSettingsPayload):
    """
    POST API to store global settings.
    Stores or updates azureGitCred, azureBearerToken, and branch.
    """
    result = await save_global_settings(
        azureGitCred=payload.azureGitCred,
        azureBearerToken=payload.azureBearerToken,
        branch=payload.branch
    )
    return create_response(success=True, result=result, status_code=201)


@router.get('/globalSettings', response_model=dict)
async def get_global_settings_data():
    """
    GET API to retrieve all three strings (azureGitCred, azureBearerToken, branch).
    """
    settings = await get_global_settings()
    if settings:
        return create_response(success=True, result=settings, status_code=200)
    return create_response(
        success=True,
        result={"azureGitCred": None, "azureBearerToken": None, "branch": None},
        status_code=200
    )

