from .BaseDataModel import BaseDataModel
import os
from .enums.ConversationEnum import ConversationEnum
from .db_shcemas.conversation import Conversation
import math


class ConversationModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client(ConversationEnum.COLLECTION_PROJECT_NAME)

        self.db = self.db_client["cluster0"]
        self.collection = self.db["conversations"]

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        return instance

    async def create_conversation(self, conversation: Conversation):
        try:
            result = await self.collection.insert_one(conversation.to_dict())
            conversation["_id"] = str(result.insert_id)
            return conversation
        except Exception as e:
            return ConversationEnum.CREATE_CONVERSATION_FAILED

    async def get_conversation_or_create_one(self, conversation_id: str):
        try:
            conversation = await self.collection.find_one(
                {"conversation_id": conversation_id}
            )
            if "_id" in conversation:
                conversation["_id"] = str(conversation["_id"])
                return conversation
            
        except Exception as e:
            return ConversationEnum.FAILED_GET_CONVERSATION_OR_CREATE_ONE

    async def get_all_conversations(self, page: int = 1, page_size: int = 10):
        try:
            total_documents = await self.collection.count_documents({})
            total_pages = math.ceil(total_documents / page_size)
            skip_value = (page - 1) * page_size
            cursor = self.collection.find({}).skip(skip_value).limit(page_size)
            conversations = await cursor.to_list(length=page_size)
            for conversation in conversations:
                conversation["_id"] = str(conversation["_id"])

            return conversations, total_pages
        except Exception as e:
            return ConversationEnum.FAILED_GET_ALL_CONVERSATIONS