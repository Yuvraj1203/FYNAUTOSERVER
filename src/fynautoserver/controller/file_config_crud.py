from fastapi import FastAPI , APIRouter, UploadFile, File
from typing import List
import os

async def files_upload(tenantId:str, tenancyName:str,files: List[UploadFile] = File(...)):
    UPLOAD_DIR = f"src/tenant/tenants/{tenancyName}"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    try:
        saved = []
        for file in files:
            print(f"Received file: {file.filename}")
            contents = await file.read()
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as f:
                f.write(contents)
            saved.append(file.filename)
        return {"uploaded": saved,'message':'file uploaded successfully'}
    except Exception as e:
        print(f'error on file_upload {e}')