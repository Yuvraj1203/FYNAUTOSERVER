from typing import List
from fynautoserver.schemas.index import Fonts
async def create_fonts_db(Tenantid:str,tenancyname:str,public_urls:List[str]):
    fonts=Fonts(
        tenantId=Tenantid or None,
        tenancyName=tenancyname or None,
        font_file_path=public_urls or []
        )
    await fonts.insert()
    return "Fonts File Uploaded Successfully"

