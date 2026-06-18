from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os
from controllers import DataController
import aiofiles
from models import ResponseSignal
from src.models import ConversationModel
import logging
from .schemas.conversation import getConversationsRequest

conversation_router=APIRouter(prefix="/api/v1/conversation",tags=['api_v1',"conversation"])

@conversation_router.get('/all')
async def get_all(request:Request):
    page=request.page
    page_size=request.page_size
    conversation_model= await ConversationModel.create_instance(
        db_client=request.app.db_client
    )
    conversations=await conversation_model.get_all_conversations(page=page,page_size=page_size)
    return conversations