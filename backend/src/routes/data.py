from fastapi import FastAPI, APIRouter, Depends,UploadFile,status
import os
from src.config import Settings, get_settings
from fastapi.responses import JSONResponse
from src.controllers import DataController,ConversationController
data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1"])

@data_router.post('/upload/{conversation_id}')
async def upload(file:UploadFile,conversation_id:str,app_settings:Settings=Depends(get_settings)):
    is_valid,signal=DataController().validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(status=status.HTTP_400_BAD_REQUEST,content={"signal":signal})
    project_dir_path=ConversationController().get_conversation_path(conversation_id=conversation_id)
