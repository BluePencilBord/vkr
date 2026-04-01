from pydantic import BaseModel, EmailStr, ConfigDict
import uuid
from datetime import datetime


class CreateUser(BaseModel):
    email: EmailStr
    password: str

class CreateUserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
    