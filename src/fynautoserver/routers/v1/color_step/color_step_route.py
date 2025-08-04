from fastapi import APIRouter
from fynautoserver.models.index import ThemeSchema
from fynautoserver.models.index import ResponseModel
from fynautoserver.crud.colors_crud import create_colors_db
from fynautoserver.utils.index import create_response

color_router=APIRouter()

@color_router.post("/createColors",response_model=ResponseModel)
async def create_colors(tenantId:str,tenancyName:str,theme:ThemeSchema):
    try:
        response=await create_colors_db(tenantId,tenancyName,theme)
        return create_response(success=True, result=response, status_code=200)

    except Exception as e:
        print(f"❌ Error in create_fonts: {e}")
        return create_response(
            success=False,
            error_message="Failed to upload fonts",
            error_detail=str(e),
            status_code=500
        )
