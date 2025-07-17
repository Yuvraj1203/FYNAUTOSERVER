from typing import List
from fynautoserver.schemas.index import Fonts
async def create_fonts_db(tenantId:str,tenancyName:str,publicUrls:List[str]):
    fonts=Fonts(
        tenantId=tenantId or None,
        tenancyName=tenancyName or None,
        font_file_path=publicUrls or []
        )
    await fonts.insert()
    return {"message":'Fonts File Uploaded Successfully'}

