from pydantic import Field,BaseModel,validator
from typing import Optional,List
from bson.objectid import ObjectId
import datetime

class Conversation(BaseModel):
    _id:Optional[ObjectId]
    conversation_name: Optional[str]
    created_at:datetime.datetime
    updated_at: datetime.datetime 
    favorite:bool
    messages:List
    
    class Config:
        arbitrary_types_allowed=True