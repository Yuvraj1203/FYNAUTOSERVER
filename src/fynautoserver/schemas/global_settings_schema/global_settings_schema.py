from beanie import Document
from typing import Optional


class GlobalSettingsSchema(Document):
    azureGitCred: Optional[str] = None
    azureBearerToken: Optional[str] = None
    branch: Optional[str] = None

    class Settings:
        name = 'global_settings'

