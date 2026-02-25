from fynautoserver.schemas.global_settings_schema.global_settings_schema import GlobalSettingsSchema
from typing import Optional


async def save_global_settings(
    azureGitCred: Optional[str],
    azureBearerToken: Optional[str],
    branch: Optional[str]
) -> dict:
    """
    Save global settings. If a document exists, it will be updated;
    otherwise, a new document will be created.
    """
    # Try to find existing document
    existing = await GlobalSettingsSchema.find_one()
    
    if existing:
        # Update existing document
        if azureGitCred is not None:
            existing.azureGitCred = azureGitCred
        if azureBearerToken is not None:
            existing.azureBearerToken = azureBearerToken
        if branch is not None:
            existing.branch = branch
        await existing.save()
        return {"message": "Global settings updated successfully"}
    else:
        # Create new document
        settings = GlobalSettingsSchema(
            azureGitCred=azureGitCred,
            azureBearerToken=azureBearerToken,
            branch=branch
        )
        await settings.insert()
        return {"message": "Global settings saved successfully"}


async def get_global_settings() -> Optional[dict]:
    """
    Get the global settings. Returns a single document with all three fields.
    """
    settings = await GlobalSettingsSchema.find_one()
    
    if settings:
        return {
            "azureGitCred": settings.azureGitCred,
            "azureBearerToken": settings.azureBearerToken,
            "branch": settings.branch
        }
    return None

