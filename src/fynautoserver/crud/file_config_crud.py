from fastapi import FastAPI , APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import base64
from fastapi.responses import JSONResponse

async def files_upload(tenantId:str, tenancyName:str,files: List[UploadFile] = File(...)):
    UPLOAD_DIR = f"src/tenant/tenants/{tenancyName}"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    try:
        saved = []
        for file in files:
            contents = await file.read()
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as f:
                f.write(contents)
            saved.append(file.filename)
        return {"uploaded": saved,'message':'file uploaded successfully'}
    except Exception as e:
        print(f'error on file_upload {e}')

def read_file_base64(file_path: str):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def find_file_by_name(root_folder: str, target_filename: str):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename == target_filename:
                return os.path.join(dirpath, filename)
    return None

def find_firebase_adminsdk_file(root_folder: str):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if "-firebase-adminsdk-" in filename:
                return os.path.join(dirpath, filename)
    return None


async def get_congif_files(tenancyName:str):
    base_path = f"src/tenant/tenants/{tenancyName}"
    dotplistFile = find_file_by_name(base_path, "GoogleService-Info.plist")
    dotjsonFile = find_file_by_name(base_path, "google-services.json")
    firebaseFile = find_firebase_adminsdk_file(base_path)

    if not any([dotplistFile, dotjsonFile, firebaseFile]):
        return {'message':'No files Found','success': False,}

    response_data = {
        "googleServiceInfoPlist": read_file_base64(dotplistFile) if dotplistFile else None,
        "googleServicesJson": read_file_base64(dotjsonFile) if dotjsonFile else None,
        "firebaseAdminsdkJson": read_file_base64(firebaseFile) if firebaseFile else None,
        'success': True,
    }

    return response_data

async def delete_File(tenantId:str, tenancyName:str,fileName:str):
    base_path = f"src/tenant/tenants/{tenancyName}"

    try:
        # Handle special case for firebase-adminsdk.json
        if fileName == "firebase-adminsdk.json":
            for dirpath, dirnames, filenames in os.walk(base_path):
                for fname in filenames:
                    if "firebase-adminsdk" in fname:
                        firebase_path = os.path.join(dirpath, fname)
                        os.remove(firebase_path)
                        return {"message": f"{fname} deleted successfully (firebase-adminsdk)"}
            return {"message": "firebase-adminsdk file not found"}

        # Handle normal case
        file_path = os.path.join(base_path, fileName)
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"message": f"{fileName} deleted successfully"}
        else:
            return {"message": "File not found"}

    except Exception as e:
        return {"message": f"Error deleting file: {str(e)}"}
    