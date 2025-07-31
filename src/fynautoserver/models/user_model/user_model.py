from pydantic import BaseModel
from typing import Optional

class UserModel(BaseModel):
    username: str
    password: str
    # refresh_token: Optional[str]
    # created_at: Optional[str]