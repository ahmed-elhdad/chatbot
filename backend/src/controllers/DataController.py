from .BaseController import BaseController
from fastapi import UploadFile
from src.routes.models import ResponseSignal
class DataController(BaseController):
    def __int__(self):
        super.__init__()
        self.size_scaled=1048567 #convert to bytes
    def validate_uploaded_file(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False,ResponseSignal.FILE_TYPE_NOT_SUPPORTED
        if file.size>self.app_settings.FILE_MAX_SIZE*self.size_scale:
            return False,ResponseSignal.FILE_SIZE_EXCEEDED
        return True 