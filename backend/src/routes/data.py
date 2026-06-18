from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
import os
import aiofiles
from src.config import Settings, get_settings
from fastapi.responses import JSONResponse
from src.controllers import DataController,ConversationController
from src.models import ConversationModel
import logging
from src.models import ResponseSignal

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1",'data'])
logger = logging.getLogger('uvicorn.error')

@data_router.post('/upload/{conversation_id}')
async def upload(request:Request,file:UploadFile,conversation_id:str,app_settings:Settings=Depends(get_settings)):
    try:
        db_client=request.app.state.db_client
        conversation_model = await ConversationModel.create_instance(
        db_client=db_client
        )
        conversation_model= ConversationModel()
        conversation = await conversation_model.get_conversation_or_create_one(
            conversation_id=conversation_id
        )
        data_controller = DataController()
        is_valid, result_signal = data_controller.validate_uploaded_file(file=file)
        if not is_valid:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": result_signal
                }
            )
        conversation_dir_path = ConversationController().get_conversation_path(
            conversation_id=conversation_id
        )
        # ensure parent directory exists
        dirpath = os.path.dirname(conversation_dir_path)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)

        try:
            async with aiofiles.open(conversation_dir_path, "wb") as f:
                while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                    await f.write(chunk)
        except Exception as e:
            logger.error(f"Error while uploading file: {e}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value},
            )

        # success
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value},
        )
    except Exception as e:
        logger.exception("Unhandled error in upload route")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"signal": str(e)},
        )

['__annotations__', '__class__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_state']