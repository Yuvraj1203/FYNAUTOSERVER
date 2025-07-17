from fastapi import APIRouter,UploadFile,File
from fynautoserver.models.index import ResponseModel
from fynautoserver.utils.index import create_response
from typing import List
from fontTools.ttLib import TTFont
from io import BytesIO
from fynautoserver.path_config import UPLOAD_DIR
from fynautoserver.crud.fonts_crud import create_fonts_db
import os
from uuid import uuid4

fonts_router=APIRouter()

@fonts_router.post("/createFonts",response_model=ResponseModel)
async def create_fonts(tenantId:str,tenancyName:str,files: List[UploadFile] = File(...)):
    try:
        public_urls = []

        for file in files:
            # Validate TTF content
            contents = await file.read()  # await only once here
            try:
                font = TTFont(BytesIO(contents))
                font.close()
            except Exception as e:
                raise ValueError(f"{file.filename} is not a valid TTF file: {e}")

            # Save file
            file_ext = file.filename.split(".")[-1]
            new_filename = f"{uuid4().hex}.{file_ext}"
            save_path = os.path.join(UPLOAD_DIR, new_filename)

            with open(save_path, "wb") as buffer:
                buffer.write(contents)

            public_urls.append(f"src/tenant/tenants/{tenancyName}/assets/fonts")

        # Insert into DB
        data = await create_fonts_db(tenantId,tenancyName,public_urls)
        return create_response(success=True, result=data, status_code=200)

    except Exception as e:
        print(f"❌ Error in create_fonts: {e}")
        return create_response(
            success=False,
            error_message="Failed to upload fonts",
            error_detail=str(e),
            status_code=500
        )