from beanie import Document
from typing import Optional,List

class Fonts(Document):
    tenantId: str
    tenancyName:str
    font_file_path:Optional[List[str]]=[]
    class Settings:
        name = 'Fonts'
