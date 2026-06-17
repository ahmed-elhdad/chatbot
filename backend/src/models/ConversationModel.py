from .BaseDataModel import BaseDataModel
import os
from .enums import DataBaseEnum
class ConversationModel(BaseDataModel):
    def __init__(self,db_client:str):
        super().__init__(db_client=self.db_client)
        self.collection=self.db_client(DataBaseEnum.COLLECTION_PROJECT_NAME.value)
    def create_conversation(self,conversation_id):