from .BaseDataModel import BaseDataModel
import os
from .enums import DataBaseEnum
from .db_shcemas.conversation import Conversation
import math


class ConversationModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=self.db_client)
        self.collection = self.db_client(DataBaseEnum.COLLECTION_PROJECT_NAME.value)

        self.db = self.db_client["cluster0"]
        self.collection = self.db["conversations"]

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        return instance

    async def create_conversation(self, conversation: Conversation):
        result = await self.collection.insert_one(conversation.to_dict())
        conversation["_id"] = str(result.insert_id)
        return conversation

    async def get_conversation_or_create_one(self, conversation_id: str):
        conversation = await self.collection.find_one(
            {"conversation_id": conversation_id}
        )
        if "_id" in conversation:
            conversation["_id"] = str(conversation["_id"])
            return conversation

    async def get_all_conversations(self, page: int = 1, page_size: int = 10):
        total_documents = await self.collection.count_documents({})
        total_pages = math.ceil(total_documents / page_size)
        skip_value = (page - 1) * page_size
        cursor = self.collection.find({}).skip(skip_value).limit(page_size)
        conversations = await cursor.to_list(length=page_size)
        for conversation in conversations:
            conversation["_id"] = str(conversation["_id"])

        return conversations, total_pages
