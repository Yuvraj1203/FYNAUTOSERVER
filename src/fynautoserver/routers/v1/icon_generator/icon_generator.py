from fastapi import APIRouter, UploadFile, File
from fynautoserver.models.index import ResponseModel
from fynautoserver.crud.icon_generator_crud import generate_icons_crud
from fynautoserver.utils.index import create_response

icon_gen_router= APIRouter()

@icon_gen_router.post('/iconGenerator',response_model=ResponseModel)
async def iconGenerator(
    tenantId:str,tenancyName:str,
    app_icon: UploadFile = File(...),
    notification_icon: UploadFile = File(...)
):
    reponse = await generate_icons_crud(tenantId,tenancyName,app_icon,notification_icon)
    return create_response(success=True, result=reponse, status_code=200)