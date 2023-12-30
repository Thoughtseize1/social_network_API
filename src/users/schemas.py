import uuid
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from fastapi_users import schemas


class UserSchemaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    created_at: datetime
    updated_at: datetime | None


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    pass
