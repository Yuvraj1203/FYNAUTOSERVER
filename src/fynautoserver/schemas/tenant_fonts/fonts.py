from beanie import Document
from typing import Optional,List

class Fonts(Document):
    tenantId: str
    tenancyName:str
    lightFontPath:Optional[str]=None
    regularFontPath:Optional[str]=None
    boldFontPath:Optional[str]=None
    class Settings:
        name = 'Fonts'
