from pydantic import BaseModel, Field
from typing import Optional
from fynautoserver.schemas.user_schema.user_schema import UserRoleEnum

class UserModel(BaseModel):
    username: str
    password: str
    role: Optional[UserRoleEnum] = "DEVCreator" 
    refreshToken: Optional[str] = None
    # created_at: Optional[str]

class LoginModel(BaseModel):
    username: str
    password: str