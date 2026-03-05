from pydantic import BaseModel
from typing import List

class ReleaseTenantCreateModel(BaseModel):
    name: str
    status: int
    androidVersion: str
    iosVersion: str
    matchBranch: str

class ReleaseTenantsModel(BaseModel):
    id: str
    name: str
    status: int
    androidVersion: str
    iosVersion: str
    matchBranch: str

class ReleaseTenantsListModel(BaseModel):
    id: str
    version: str
    tenants: List[ReleaseTenantsModel]

class TenantStatusUpdateModel(BaseModel):
    """Request model for updating tenant status and versions"""
    name: str  # Tenant name to search
    status: int  # New status to update (0=pending, 1=onGoing, 2=published, 3=failed)
    android: bool = False  # Whether to increment android version
    ios: bool = False  # Whether to increment iOS version


def increment_version(version: str) -> str:
    """
    Increment version number.
    Examples:
        "1.0.0" -> "1.0.1"
        "1.0.9" -> "1.1.0"
        "1.9.9" -> "2.0.0"
    """
    parts = version.split('.')
    if len(parts) != 3:
        return version
    
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    
    patch += 1
    if patch > 9:
        patch = 0
        minor += 1
        if minor > 9:
            minor = 0
            major += 1
    
    return f"{major}.{minor}.{patch}"


def decrement_version(version: str) -> str:
    """
    Decrement version number.
    Examples:
        "1.0.1" -> "1.0.0"
        "1.1.0" -> "1.0.9"
        "2.0.0" -> "1.9.9"
    """
    parts = version.split('.')
    if len(parts) != 3:
        return version
    
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    
    patch -= 1
    if patch < 0:
        patch = 9
        minor -= 1
        if minor < 0:
            minor = 9
            major -= 1
            if major < 0:
                return "0.0.0"
    
    return f"{major}.{minor}.{patch}"
