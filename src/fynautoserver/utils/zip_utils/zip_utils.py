from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import zipfile
import os
import io

def zip_folder(folder_path, output_zip_path):
    # with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    #     for root, _, files in os.walk(folder_path):
    #         for file in files:
    #             abs_path = os.path.join(root, file)
    #             rel_path = os.path.relpath(abs_path, folder_path)
    #             zipf.write(abs_path, rel_path)

    
    # Create an in-memory zip
    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, folder_path)
                zipf.write(abs_path, rel_path)
    zip_io.seek(0)

    return StreamingResponse(
        zip_io,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename={output_zip_path}"}
    )
    return output_zip_path