from beanie import Document
from typing import Optional
from enum import Enum

class UserRoleEnum(str, Enum):
    admin = "Admin"
    creator = "Creator"
    viewer = "Viewer"

class UserSchema(Document):
    username: str
    password: str
    role: Optional[UserRoleEnum] = "Creator" 

    class Settings:
        name = 'Users'