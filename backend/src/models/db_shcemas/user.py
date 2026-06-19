from .conversation import ConfigDict, PyObjectId
from typing import Optional
import datetime
from pydantic import BaseModel, EmailStr, Field, constr

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    hashed_password: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)