from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import List

class NoteBase(BaseModel):
    """
    Inherits title/body/tags validators from NoteBase intentionally:
    a note read from the DB should satisfy the same validations as one
    being written. If a stored note ever fails these checks, that's a
    signal something bypassed validation on the way in and not a bug in
    the read path.
    """
    title: str
    body: str
    tags: List[str] = []

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title must not be empty")
        if len(v) > 200:
            raise ValueError("title must be 200 characters or fewer")
        return v

    @field_validator("body")
    @classmethod
    def body_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("body must not be empty")
        return v

    @field_validator("tags")
    @classmethod
    def tags_limit(cls, v: List[str]) -> List[str]:
        if len(v) > 20:
            raise ValueError("a note may have at most 20 tags")
        return v
    

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class NoteOut(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    @field_validator("tags", mode="before")
    @classmethod
    def split_tags(cls, v):
        if isinstance(v, str):
            return [t.strip() for t in v.split(",") if t.strip()]
        return v
    
    model_config = ConfigDict(from_attributes=True)