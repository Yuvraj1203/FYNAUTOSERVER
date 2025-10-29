from beanie import Document
from typing import Optional

class TenantInfoSchema(Document):
    androidVersionCode:str
    androidVersionName:str
    apiUrl: str
    appName: str
    auth0ClientId: str
    auth0Domain: str
    auth0Organization: Optional[str] = None
    bundleId: str
    iosTeamId : str
    iosVersionCode: str
    iosVersionName: str
    oktaClientId: Optional[str] = None
    oktaDomain: Optional[str] = None
    oktaTenancyName: Optional[str] = None
    packageName: str
    sentryDsn: str
    tenancyName: str
    tenantId: str

    class Settings:
        name = 'tenant_info'