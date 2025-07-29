from fastapi import APIRouter,UploadFile,File, Form
from fynautoserver.models.index import ResponseModel
from fynautoserver.utils.index import create_response
from typing import List
from fontTools.ttLib import TTFont
from io import BytesIO
from fynautoserver.path_config import SRC_DIR
from fynautoserver.crud.fonts_crud import create_fonts_db,update_index_tsx
import os, shutil
from fynautoserver.schemas.index import Fonts
from typing import Optional

fonts_router=APIRouter()

@fonts_router.post("/createFonts",response_model=ResponseModel)
async def create_fonts(
                        tenantId: str ,
                        tenancyName: str ,
                        defaultFont: bool = False,
                        defaultFontName: Optional[str] = 'other',
                        lightFont: Optional[UploadFile] = File(None),
                        regularFont: Optional[UploadFile] = File(None),
                        boldFont: Optional[UploadFile] = File(None),
                       ):
    try:
        existing=await Fonts.find_one({"tenantId": tenantId})
        existing.defaultFontName = defaultFontName
        if existing:
            if defaultFont:
                # Remove the old font if it exists
                old_font_sub_path = f"tenant/tenants/{tenancyName}/assets/fonts/AppFont"
                old_font_path = os.path.join(SRC_DIR, old_font_sub_path)
                if os.path.exists(old_font_path) and os.path.isdir(old_font_path):
                    shutil.rmtree(old_font_path)

                # add the whole font folder to this
                source_folder_Assets = os.path.join(SRC_DIR, f"tenant/customFonts/{defaultFontName}")
                destination_folder_Assets =  f"src/tenant/tenants/{tenancyName}/assets/fonts/AppFont"
                shutil.copytree(source_folder_Assets, destination_folder_Assets,dirs_exist_ok=True)

                # Update DB record with new font path and name
                destination_folder_for_db =  f"tenant/tenants/{tenancyName}/assets/fonts/AppFont"
                existing.lightFontPath = os.path.join(destination_folder_for_db, 'light.ttf')
                existing.regularFontPath = os.path.join(destination_folder_for_db, 'regular.ttf')
                existing.boldFontPath = os.path.join(destination_folder_for_db, 'bold.ttf')
                await existing.save()  # or your DB update logic

                for weight in ["light", "regular", "bold"]:
                    # Optionally update your index.tsx or other metadata
                    update_index_tsx(f'{weight}.ttf', tenancyName,weight)
            
            else:
                if lightFont:
                    contents = await lightFont.read()  # read once
                    try:
                        font = TTFont(BytesIO(contents))
                        font.close()
                    except Exception as e:
                        raise ValueError(f"{lightFont.filename} is not a valid TTF file: {e}")

                    # Define the target folder
                    fonts_folder = f"tenant/tenants/{tenancyName}/assets/fonts/AppFont"
                    folder_path = os.path.join(SRC_DIR, fonts_folder)
                    os.makedirs(folder_path, exist_ok=True)

                    # Remove the old font if it exists
                    if existing.lightFontPath:
                        old_font_path = os.path.join(SRC_DIR, existing.lightFontPath)
                        if os.path.exists(old_font_path):
                            os.remove(old_font_path)

                    # Save new light font file
                    new_font_path = os.path.join(folder_path, lightFont.filename)
                    with open(new_font_path, "wb") as buffer:
                        buffer.write(contents)

                    # Update DB record with new font path and name
                    new_relative_path = os.path.join(fonts_folder, lightFont.filename)
                    existing.lightFontPath = new_relative_path
                    await existing.save()  # or your DB update logic

                    # Optionally update your index.tsx or other metadata
                    update_index_tsx(lightFont.filename, tenancyName,"Light")

                if regularFont:
                    # Validate TTF content
                    contents = await regularFont.read()  # read once
                    try:
                        font = TTFont(BytesIO(contents))
                        font.close()
                    except Exception as e:
                        raise ValueError(f"{regularFont.filename} is not a valid TTF file: {e}")

                    # Define the target folder
                    fonts_folder = f"tenant/tenants/{tenancyName}/assets/fonts/AppFont"
                    folder_path = os.path.join(SRC_DIR, fonts_folder)
                    os.makedirs(folder_path, exist_ok=True)

                    # Remove the old font if it exists
                    if existing.regularFontPath:
                        old_font_path = os.path.join(SRC_DIR, existing.regularFontPath)
                        if os.path.exists(old_font_path):
                            os.remove(old_font_path)

                    # Save new light font file
                    new_font_path = os.path.join(folder_path, regularFont.filename)
                    with open(new_font_path, "wb") as buffer:
                        buffer.write(contents)

                    # Update DB record with new font path and name
                    new_relative_path = os.path.join(fonts_folder, regularFont.filename)
                    existing.regularFontPath = new_relative_path
                    await existing.save()  # or your DB update logic

                    # Optionally update your index.tsx or other metadata
                    update_index_tsx(regularFont.filename, tenancyName,"Regular")

                if boldFont:
                    # Validate TTF content
                    contents = await boldFont.read()  # read once
                    try:
                        font = TTFont(BytesIO(contents))
                        font.close()
                    except Exception as e:
                        raise ValueError(f"{boldFont.filename} is not a valid TTF file: {e}")

                    # Define the target folder
                    fonts_folder = f"tenant/tenants/{tenancyName}/assets/fonts/AppFont"
                    folder_path = os.path.join(SRC_DIR, fonts_folder)
                    os.makedirs(folder_path, exist_ok=True)

                    # Remove the old font if it exists
                    if existing.boldFontPath:
                        old_font_path = os.path.join(SRC_DIR, existing.boldFontPath)
                        if os.path.exists(old_font_path):
                            os.remove(old_font_path)

                    # Save new light font file
                    new_font_path = os.path.join(folder_path, boldFont.filename)
                    with open(new_font_path, "wb") as buffer:
                        buffer.write(contents)

                    # Update DB record with new font path and name
                    new_relative_path = os.path.join(fonts_folder, boldFont.filename)
                    existing.boldFontPath = new_relative_path
                    await existing.save()  # or your DB update logic

                    # Optionally update your index.tsx or other metadata
                    update_index_tsx(boldFont.filename, tenancyName,"Bold")
            
            response = existing.model_dump()
            response['id'] = str(response['id'])
            return create_response(success=True,result={'message':"Font Path Updated Successfully",'fontsData':response},status_code=200)
        else:
            if defaultFont:
                # Remove the old font if it exists
                old_font_path = f"tenant/tenants/{tenancyName}/assets/fonts/AppFont"
                if os.path.exists(old_font_path):
                    os.remove(old_font_path)

                # add the whole font folder to this
                source_folder_Assets = f"src/tenant/customFonts/{defaultFontName}"
                destination_folder_Assets =  f"tenant/tenants/{tenancyName}/assets/fonts/AppFont"
                shutil.copytree(source_folder_Assets, destination_folder_Assets,dirs_exist_ok=True)

                # Update DB record with new font path and name
                lightFontPath = os.path.join(destination_folder_Assets, 'light.ttf')
                regularFontPath = os.path.join(destination_folder_Assets, 'regular.ttf')
                boldFontPath = os.path.join(destination_folder_Assets, 'bold.ttf')

                for weight in ["light", "regular", "bold"]:
                    # Optionally update your index.tsx or other metadata
                    update_index_tsx(f'{weight}.ttf', tenancyName,weight)
                
                # Insert into DB
                data = await create_fonts_db(tenantId,tenancyName,defaultFontName,lightFontPath,regularFontPath,boldFontPath)
                return create_response(success=True, result=data, status_code=200)
            
            else:
                if lightFont:
                    contents = await lightFont.read()  # await only once here
                    try:
                        font = TTFont(BytesIO(contents))
                        font.close()
                    except Exception as e:
                        raise ValueError(f"{lightFont.filename} is not a valid TTF file: {e}")

                    # Save file
                    fonts_folder = f"tenant/tenants/{tenancyName}/assets/fonts/AppFont"
                    folder_path = os.path.join(SRC_DIR, fonts_folder)
                    os.makedirs(folder_path, exist_ok=True)  # ensure directory exists

                    save_path = os.path.join(folder_path, lightFont.filename)

                    with open(save_path, "wb") as buffer:
                        buffer.write(contents)
                    update_index_tsx(lightFont.filename,tenancyName,"Light")
                    lightFontPath=os.path.join(fonts_folder, lightFont.filename)
                if regularFont:
                    # Validate TTF content
                    contents = await regularFont.read()  # await only once here
                    try:
                        font = TTFont(BytesIO(contents))
                        font.close()
                    except Exception as e:
                        raise ValueError(f"{regularFont.filename} is not a valid TTF file: {e}")

                    # Save file
                    fonts_folder = f"tenant/tenants/{tenancyName}/assets/fonts/AppFont"
                    folder_path = os.path.join(SRC_DIR, fonts_folder)
                    os.makedirs(folder_path, exist_ok=True)  # ensure directory exists

                    save_path = os.path.join(folder_path, regularFont.filename)

                    with open(save_path, "wb") as buffer:
                        buffer.write(contents)
                    update_index_tsx(regularFont.filename,tenancyName,"Regular")
                    regularFontPath=os.path.join(fonts_folder, regularFont.filename)
                if boldFont:
                    # Validate TTF content
                    contents = await boldFont.read()  # await only once here
                    try:
                        font = TTFont(BytesIO(contents))
                        font.close()
                    except Exception as e:
                        raise ValueError(f"{boldFont.filename} is not a valid TTF file: {e}")

                    # Save file
                    fonts_folder = f"tenant/tenants/{tenancyName}/assets/fonts/AppFont"
                    folder_path = os.path.join(SRC_DIR, fonts_folder)
                    os.makedirs(folder_path, exist_ok=True)  # ensure directory exists

                    save_path = os.path.join(folder_path, boldFont.filename)

                    with open(save_path, "wb") as buffer:
                        buffer.write(contents)
                    update_index_tsx(boldFont.filename,tenancyName,"Bold")
                    boldFontPath=os.path.join(fonts_folder, boldFont.filename)

                # Insert into DB
                data = await create_fonts_db(tenantId,tenancyName,defaultFontName,lightFontPath,regularFontPath,boldFontPath)
                return create_response(success=True, result=data, status_code=200)
                

    except Exception as e:
        print(f"❌ Error in create_fonts: {e}")
        return create_response(
            success=False,
            error_message="Failed to upload fonts",
            error_detail=str(e),
            status_code=500
        )