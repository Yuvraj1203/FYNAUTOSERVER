from fastapi import APIRouter, UploadFile, File
from fynautoserver.models.index import ResponseModel
from fynautoserver.crud.icon_generator_crud import generate_icons_crud
from fynautoserver.utils.index import create_response
import os
from fastapi.responses import FileResponse
from fynautoserver.path_config import SRC_DIR

icon_gen_router= APIRouter()

@icon_gen_router.post('/iconGenerator',response_model=ResponseModel)
async def iconGenerator(
    tenantId:str,tenancyName:str,
    app_icon: UploadFile = File(...),
    notification_icon: UploadFile = File(...),
    app_banner: UploadFile = File(...)
):
    reponse = await generate_icons_crud(tenantId,tenancyName,app_icon,notification_icon,app_banner)
    return create_response(success=True, result=reponse, status_code=200)