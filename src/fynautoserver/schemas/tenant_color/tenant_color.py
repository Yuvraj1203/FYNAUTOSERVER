from beanie import Document
from fynautoserver.models.index import color_schema
from typing import Optional

class Color(Document):
    tenantId:str
    tenancyName:str
    light:Optional[color_schema]=None
    dark:Optional[color_schema]=None
    filePath:Optional[str]=None
    class Settings:
        name = 'Colors'