
from pydantic import BaseModel
class ChunkResult(BaseModel):
    type: str          
    content: str       
    image_url: str = None 