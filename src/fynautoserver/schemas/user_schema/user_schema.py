from beanie import Document
from typing import Optional

class UserSchema(Document):
    username: str
    password: str

    class Settings:
        name = 'Users'