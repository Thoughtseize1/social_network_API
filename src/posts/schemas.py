import uuid
from pydantic import BaseModel
from datetime import datetime


class PostSchemaBase(BaseModel):
    text: str


class PostSchemaCreate(PostSchemaBase):
    pass


class PostSchemaUpdate(PostSchemaBase):
    pass


class PostSchemaResponse(PostSchemaBase):
    id: int
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes: True


class PostSchemaDB(PostSchemaBase):
    id: int
    owner_id: uuid.UUID
    text: str
    created_at: datetime
    updated_at: datetime | None
