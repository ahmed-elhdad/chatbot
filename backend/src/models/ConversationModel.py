from .BaseDataModel import BaseDataModel
import os
from .enums import DataBaseEnum
from .db_shcemas import Conversation
class ConversationModel(BaseDataModel):
    def __init__(self,db_client:str):
        super().__init__(db_client=self.db_client)
        self.collection=self.db_client(DataBaseEnum.COLLECTION_PROJECT_NAME.value)
    async def create_conversation(self,conversation:Conversation):
        result=await self.collection.insert_one(conversation.to_dict())
        conversation._id=result.insert_id
        return conversation
    