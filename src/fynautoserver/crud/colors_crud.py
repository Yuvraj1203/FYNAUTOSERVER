from fynautoserver.models.index import ThemeSchema
from fynautoserver.schemas.index import Color

async def create_colors_db(tenant_id:str,tenancyname:str,theme:ThemeSchema):
    colors= Color(
        tenantId=tenant_id or None,
        tenancyName=tenancyname or None,
        light=theme.light or None,
        dark= theme.dark or None
    )
    await colors.insert()
    return "Colors Inserted Successfully"