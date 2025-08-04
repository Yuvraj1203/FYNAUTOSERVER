from beanie import Document
from typing import Optional
from enum import Enum

class UserRoleEnum(str, Enum):
    admin = "Admin"
    uatcreator = "UATCreator"
    devcreator = "DEVCreator"
    viewer = "Viewer"

class UserSchema(Document):
    username: str
    password: str
    role: Optional[UserRoleEnum] = "DEVCreator" 
    refreshToken: Optional[str] = None

    class Settings:
        name = 'Users'