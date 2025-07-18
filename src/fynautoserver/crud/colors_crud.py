from fynautoserver.models.index import ThemeSchema
from fynautoserver.schemas.index import Color

async def create_colors_db(tenantId:str,tenancyName:str,theme:ThemeSchema):        
    existing = await Color.find_one({"tenantId": tenantId})

    if(existing):
        existing.light=theme.light
        existing.dark=theme.dark
        await existing.save()
        return {"message":"Colors Inserted Successfully"}
    else:
        colors= Color(
        tenantId=tenantId or None,
        tenancyName=tenancyName or None,
        light=theme.light or None,
        dark= theme.dark or None
        )
        await colors.insert()
        return {"message":"Colors Inserted Successfully"}
     
