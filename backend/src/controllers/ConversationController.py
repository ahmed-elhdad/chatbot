import os
from .BaseController import BaseController
class ConversationController(BaseController):
    def __init__(self):
        super.__init__()
    def get_conversation_path(self,conversation_id:str):
        conversation_dir=os.path.join(self.files_dir,conversation_id)
        if not os.path.exists(conversation_dir):
            os.makedirs(conversation_dir)
        return conversation_dir