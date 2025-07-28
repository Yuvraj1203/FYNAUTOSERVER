import json, os
from fynautoserver.models.index import TenantInfoModel , AddTenantModel
from fynautoserver.utils.index import create_response
from fynautoserver.schemas.index import TenantInfoSchema, AddTenantSchema,StepModel, Fonts, Color
from pathlib import Path
from fastapi import  HTTPException
import httpx
from fynautoserver.utils.index import zip_folder
from fynautoserver.schemas.tenant_info_schema.add_tenant_schema import DEFAULT_STEPS
from copy import deepcopy
from typing import List
import shutil
from fynautoserver.path_config import SRC_DIR
from fynautoserver.crud.file_config_crud import get_congif_files
from fynautoserver.crud.colors_crud import get_theme_Colors

async def add_tenant(payload:AddTenantModel):
        existing = await AddTenantSchema.find_one({"tenantId": payload.tenantId})
        if existing:
            return {"message": "Tenant Already Exists"}
        else:
            payload_with_steps = payload.model_dump()
            payload_with_steps["steps"] = deepcopy(DEFAULT_STEPS)

            tenant_details = AddTenantSchema(**payload_with_steps)
            await tenant_details.insert()
                #for setting assets folder to tenat

            source_folder_Assets = f"./src/tenant/mandatory_files"
            destination_folder_Assets = f"./src/tenant/tenants/{payload.tenancyName}"
            shutil.copytree(source_folder_Assets, destination_folder_Assets,dirs_exist_ok=True)

            font_light_folder = f"tenant/tenants/{payload.tenancyName}/assets/fonts/AppFont/Quicksand-Light.ttf"
            font_regular_folder = f"tenant/tenants/{payload.tenancyName}/assets/fonts/AppFont/Quicksand-SemiBold.ttf"
            font_bold_folder = f"tenant/tenants/{payload.tenancyName}/assets/fonts/AppFont/Quicksand-Bold.ttf"
            #create
            fonts=Fonts(
                tenantId=payload.tenantId,
                tenancyName=payload.tenancyName,
                lightFontPath=font_light_folder or None,
                regularFontPath=font_regular_folder or None,
                boldFontPath=font_bold_folder or None
                )
            await fonts.insert()

            return {"message": "Tenant Added Successfully"}
    # try:

    # except Exception as e:
    #     print(f'error from add_tenant due to : {e}')

async def create_tenant_folder(payload:TenantInfoModel):
    name_no_spaces = payload.tenancyName.replace(" ", "")
    folder_path = Path(f"./src/tenant/tenants/{name_no_spaces}")
    zip_folder_path = Path(f"src/tenant/tenant_zip/{name_no_spaces}.zip")

    # Create the directory (including any intermediate directories)
    folder_path.mkdir(parents=True, exist_ok=True)  # parents=True creates intermediate directories if needed

    # Define the file path
    file_path = folder_path / 'tenantInfo.json'

    with open(file_path,'w') as file:
        try:
            json.dump(payload.dict(), file, indent=4)
            file.flush()  # ✅ Ensure data is written to disk
            os.fsync(file.fileno())  # ✅ Especially important on some systems
            zip_folder(folder_path,zip_folder_path)
            return
        except Exception as e:
            return create_response(
                success=False,
                error_message="File creation failed",
                error_detail=str(e),
                status_code=500,
            )

async def create_tenant_info(payload:TenantInfoModel):
    try:
        existing = await TenantInfoSchema.find_one(TenantInfoSchema.tenantId == payload.tenantId)

        if existing:
        # Update existing fields with new data
            for field, value in payload.model_dump().items():
                setattr(existing, field, value)
            await existing.save()
            data = existing.model_dump()
            data["id"] = str(existing.id)
            await create_tenant_folder(payload)
            return {"message": "Tenant Info Updated",'tenantFormData':data}
        else:
            tenant_info = TenantInfoSchema(**payload.model_dump())
            response = await tenant_info.insert()
            response = response.model_dump()
            response["id"]=str(response["id"])
            await create_tenant_folder(payload)
            return {"message": "Tenant Info Inserted",'tenantFormData':response}


    except Exception as e:
        print(f'error from create_tenant_info due to : {e}')


async def getTenantInfoByTenancyName(tenancyName : str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://aa.fyndev.com/api/services/app/User/gettenantidbyname",
                params={"TenancyName": tenancyName},
                timeout=10.0
            )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong")
    

async def remove_tenant(tenantId: str,tenancyName:str):
    tenant = await AddTenantSchema.find_one({"tenantId": tenantId})
    color_db = await Color.find_one({"tenantId": tenantId})
    font_db = await Fonts.find_one({"tenantId": tenantId})
    tenant_info_db = await TenantInfoSchema.find_one({"tenantId": tenantId})
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    await tenant.delete()
    if color_db:
        await color_db.delete()
    if font_db:
        await font_db.delete()
    if tenant_info_db:
        await tenant_info_db.delete()

    folder_path = f"src/tenant/tenants/{tenancyName}"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    return {"message": "Tenant deleted successfully"}

async def update_tenant_step(tenantId: str, step: int, steps: List[StepModel]):
    try:
        existing_tennant = await AddTenantSchema.find_one({"tenantId": tenantId})
        if not existing_tennant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        if step:
            existing_tennant.step = step
        if steps:
            existing_tennant.steps=steps
        await existing_tennant.set_status_from_steps() 
        await existing_tennant.save()
        updatedTenantTemp = await AddTenantSchema.find_one({"tenantId": tenantId})
        updatedTenant = updatedTenantTemp.model_dump()
        updatedTenant["id"] = str(updatedTenant["id"])
        return updatedTenant
    except Exception as e:
        print(f"Error during updating tenant step: {e}")
        raise HTTPException(status_code=500, detail="Failed to update tenant step")
    
async def fetch_form_data(tenantId:str,tenancyName:str):
    existing = await TenantInfoSchema.find_one({'tenantId':tenantId})
    if existing:
        existing = existing.model_dump()
        existing['id'] = str(existing['id'])
        files_config = await get_congif_files(tenancyName)
        theme_colors = get_theme_Colors(tenantId)
        return {"message":'form data fetched successfully','tenantFormData':existing,'fileConfigsData':files_config,'themeColors':theme_colors}
    else:
        return {"message":'no tenant form data found','tenantFormData':existing}