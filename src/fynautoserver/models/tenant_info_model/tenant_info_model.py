from pydantic import BaseModel , field_validator , ConfigDict
from typing import Optional

class TenantInfoModel(BaseModel):
    apiUrl: str
    appName: str
    auth0ClientId: str
    auth0Domain: str
    auth0Organization: Optional[str] = None
    bundleId: str
    oktaClientId: Optional[str] = None
    oktaDomain: Optional[str] = None
    packageName: str
    sentryDsn: str
    tenancyName: str
    tenantId: str

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda s: s[0].lower() + s[1:]  # PascalCase → camelCase
    )
    
    @field_validator("auth0Domain")
    @classmethod
    def validate_auth0_domain(cls, value):
        if ".auth0" not in value or ".com" not in value:
            raise ValueError("Please provide valid Auth0 Domain")
        return value
    
    @field_validator("bundleId", "packageName")
    @classmethod
    def validate_com_prefix_fields(cls, value: str, info) -> str:
        if not value.startswith("com."):
            raise ValueError(f"Please provide valid {info.field_name}")
        return value
