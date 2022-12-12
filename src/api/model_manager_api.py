from fastapi import APIRouter
from fastapi import UploadFile,File
import tempfile
import os
from src.model_manager.model_manager import handle_new_model
model_api_router=APIRouter(prefix="/model")

@model_api_router.post('/handle/new')
async def handle_model(file:UploadFile=File(...)):
    temp = tempfile.NamedTemporaryFile(delete=False)
    try:
        try:
            contents = file.file.read()
            with temp as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()
        handle_new_model(temp.name)
    except Exception:
        return {"message": "There was an error processing the file"}
    finally:
        os.remove(temp.name)
    return {"message": "model uploaded"}
