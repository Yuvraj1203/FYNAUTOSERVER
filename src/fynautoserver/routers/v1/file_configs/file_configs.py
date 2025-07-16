from fastapi import FastAPI , APIRouter, UploadFile, File
from typing import List
from fynautoserver.controller.file_config_crud import files_upload
from fynautoserver.utils.index import create_response

app = FastAPI()

router = APIRouter()

@router.post('/fileConfigsUpload')
async def files_configs_upload(tenantId:str, tenancyName:str,files: List[UploadFile] = File(...)):
    response = await files_upload(tenantId,tenancyName,files)
    return create_response(success=True, result=response, status_code=201)
