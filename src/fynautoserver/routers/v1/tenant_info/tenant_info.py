from fastapi import APIRouter, FastAPI
from fynautoserver.models.index import TenantInfoModel , AddTenantModel
from fynautoserver.crud.tenant_info_crud import create_tenant_info , getTenantInfoByTenancyName, add_tenant, remove_tenant,update_tenant_step, fetch_form_data
from fynautoserver.utils.index import create_response,APIExceptionHandler
from fynautoserver.models.index import ResponseModel
from fynautoserver.schemas.index import AddTenantSchema,StepModel
from fastapi.encoders import jsonable_encoder
from pymongo.errors import PyMongoError
from typing import List

app = FastAPI()

router = APIRouter()

@router.get('/getTenantInfo',response_model=ResponseModel)
async def getTenantInfo():
    try:
        # Your business logic here (e.g., DB fetch)
        data = {"msg": "hi there"}  # Replace with actual logic

        if not data:
            APIExceptionHandler.not_found("Tenant information not found.")

        return create_response(success=True, result=data)

    except PyMongoError as e:
        APIExceptionHandler.mongo_error(e)
    except Exception as e:
        APIExceptionHandler.internal_server_error(str(e))

@router.get('/getTenantIdByName')
async def getTenantIdByName(tenancyName: str):
    response = await getTenantInfoByTenancyName(tenancyName)
    return response

@router.get('/getAllTenants',response_model=ResponseModel)
async def getAllTenants():
    response = await AddTenantSchema.find_all().to_list()
    json_safe = jsonable_encoder(response)
    return create_response(success=True, result=json_safe, status_code=201)

@router.delete('/removeTenant',response_model=ResponseModel)
async def removeTenant(tenantId: str,tenancyName: str):
    response = await remove_tenant(tenantId,tenancyName)
    return create_response(success=True, result=response, status_code=201)

@router.post('/addTenant',response_model=ResponseModel)
async def addTenant(payload: AddTenantModel):
    response = await add_tenant(payload)
    return create_response(success=True, result=response, status_code=201)
    
@router.post('/setTenantInfo',response_model=ResponseModel)
async def setTenantInfo(payload:TenantInfoModel):
    try:
        tenant = await create_tenant_info(payload)
        return create_response(success=True, result=tenant, status_code=201)
    except Exception as e:
        print(f"error during creating tenant file : {e}")
        return create_response(
            success=False,
            error_message="Failed to create tenant. Please try again.",
            error_detail=str(e),
            status_code=500,
        )

@router.get('/getTenantFormData',response_model=ResponseModel)
async def getTenantFormData(tenantId:str,tenancyName:str):
    try:
        formData = await fetch_form_data(tenantId,tenancyName)
        return create_response(success=True, result=formData, status_code=201)
    except Exception as e:
        return create_response(
            success=False,
            error_message="Failed to fetch form data. Please try again.",
            error_detail=str(e),
            status_code=500,
        )
        
@router.patch("/updateTenantStep",response_model=ResponseModel)
async def updateTenantStep(tenantId:str,step:int,steps:List[StepModel]):
    try:
        tenant= await update_tenant_step(tenantId, step, steps)
        return create_response(success=True, result=tenant, status_code=200)
    except Exception as e:
        print(f"error during updating tenant step : {e}")
        return create_response(
            success=False,
            error_message="Failed to update tenant step. Please try again.",
            error_detail=str(e),
            status_code=500,
        )